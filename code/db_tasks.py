"""Design-Bench -> mbo.Task adapter. Lets the SAME surrogate x optimizer grid
(mbo.run_offline / run_o2o / run_calibration) run on real benchmarks with zero
changes to the engine. Runs only in the `db` conda env (design-bench installed).

Every task is exposed in a [0,1] design box so mbo's optimizers (which clip to
[0,1]) work untouched:
  - continuous tasks (Superconductor, Ant, DKitty, Hopper): min-max normalize x.
  - discrete tasks (TFBind8/10, GFP, UTR, ChEMBL): design = per-position class
    probabilities in [0,1]^(L*C); decode by per-position argmax before the oracle.
Scores are min-max normalized to [0,1] using the dataset range design-bench
publishes, so numbers are directly comparable to published normalized tables.
"""
import numpy as np

# Standard Design-Bench task ids (oracle variants match the COMs/DDOM tables).
# Oracle choice: TFBind8/10 use the exact discrete oracle (dep-free). Every other task
# uses design-bench's RandomForest approximate oracle -- a first-class, literature-standard
# oracle (Superconductor's canonical oracle) that avoids the exact-oracle simulator deps
# (mujoco for Ant/DKitty/Hopper, TensorFlow for GFP-Transformer/UTR-ResNet). A consistent
# RF oracle across tasks is also cleaner for a surrogate x optimizer attribution study.
# Document this in the paper. (ChEMBL omitted: its mirror oracle pickle is corrupt.)
TASKS = {
    'TFBind8':       'TFBind8-Exact-v0',
    'TFBind10':      'TFBind10-Exact-v0',   # only exact oracle exists. Its 4^10 landscape
    #   build (~98s/worker) crashes under 48-way concurrency, so TFBind10 runs in its own
    #   low-concurrency pass (see cloud/queue) while the other 7 run at full jobs.
    'Superconductor':'Superconductor-RandomForest-v0',
    'GFP':           'GFP-RandomForest-v0',
    'UTR':           'UTR-RandomForest-v0',
    'AntMorphology': 'AntMorphology-RandomForest-v0',
    'DKitty':        'DKittyMorphology-RandomForest-v0',
    'Hopper':        'HopperController-RandomForest-v0',
}

class DesignBenchTask:
    """Wraps a design_bench task in the mbo.Task interface: .name .dim .data() .oracle()."""
    def __init__(self, short_name, subsample=None):
        import design_bench
        self.name = short_name
        self._t = design_bench.make(TASKS[short_name])
        self.discrete = self._t.is_discrete

        x, y = self._t.x, self._t.y            # y: (N,1)
        self.ymin, self.ymax = float(y.min()), float(y.max())
        y01 = (y[:, 0] - self.ymin) / (self.ymax - self.ymin + 1e-12)
        if not self.discrete:
            self.xmin = x.min(0); self.xmax = x.max(0)          # from FULL data -> oracle decode box

        # Subsample the RAW dataset BEFORE the expensive one-hot/normalize. TFBind10 has
        # 4.16M rows; one-hot-encoding all of them (-> ~666MB) every build was the per-cell
        # bottleneck (run_all rebuilds the task per cell). Cap on the raw ints first, encode
        # only the survivors. Selection is bitwise-identical to encoding-then-subsampling
        # (same y01, same RandomState(0), one-hot is row-wise) -- pure speedup, no science change.
        if subsample and len(x) > subsample:                    # score-biased: top + random
            idx = np.argsort(y01)
            keep = np.concatenate([idx[-subsample//5:],
                                   np.random.RandomState(0).choice(len(x), subsample*4//5, replace=False)])
            x, y01 = x[keep], y01[keep]

        if self.discrete:
            self.L, self.C = x.shape[1], int(self._t.num_classes)
            self.dim = self.L * self.C
            x01 = self._onehot(x).reshape(len(x), -1)           # {0,1} subset of [0,1]
        else:
            self.dim = x.shape[1]
            x01 = (x - self.xmin) / (self.xmax - self.xmin + 1e-12)
        self._x = x01.astype(np.float32)
        self._y = y01.astype(np.float32)

    def _onehot(self, xint):
        oh = np.zeros((len(xint), self.L, self.C), np.float32)
        r, l = np.meshgrid(np.arange(len(xint)), np.arange(self.L), indexing='ij')
        oh[r, l, xint] = 1.0
        return oh

    def _decode(self, x01):
        """[0,1] design box -> the representation design_bench.predict expects."""
        if self.discrete:
            return x01.reshape(-1, self.L, self.C).argmax(-1)          # per-position argmax
        return x01 * (self.xmax - self.xmin) + self.xmin               # denormalize

    def data(self):
        return self._x.copy(), self._y.copy()

    def oracle(self, x01):
        x01 = np.clip(np.asarray(x01, np.float32), 0, 1)
        yv = self._t.predict(self._decode(x01))                         # (n,1) raw score
        return ((yv[:, 0] - self.ymin) / (self.ymax - self.ymin + 1e-12)).astype(np.float32)

_TASK_CACHE = {}   # per-worker memo: run_all rebuilds tasks per cell; build+encode each once instead.
def make_db_tasks(names, subsample=None):
    out = []
    for n in names:
        key = (n, subsample)
        t = _TASK_CACHE.get(key)
        if t is None:
            t = _TASK_CACHE[key] = DesignBenchTask(n, subsample=subsample)
        out.append(t)          # read-only across cells (data() copies, oracle() is pure) -> safe to share
    return out

if __name__ == '__main__':                                              # cloud-only smoke
    import sys
    names = sys.argv[1:] or ['TFBind8', 'Superconductor']
    for n in names:
        t = DesignBenchTask(n)
        x, y = t.data()
        s = t.oracle(x[:5])
        print(f'{n:16s} dim={t.dim:5d} N={len(x):6d} discrete={t.discrete} '
              f'y01=[{y.min():.2f},{y.max():.2f}] oracle(5)={np.round(s,3)}')
