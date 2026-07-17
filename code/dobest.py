"""A.1.4 -- the do-nothing baseline. For every synthetic task:
  data_best   = best NOISELESS oracle score over the whole offline dataset D
  donothing   = oracle score of the top-128 dataset points (ranked by the OBSERVED noisy y,
                the only signal an offline method sees) returned UNMODIFIED -> p100/p50
Then, from the committed camera grid (the (on,on) corner), the best grid cell's p100 per
task, and the ratio (best cell)/(data_best) and (best cell)/(donothing p100).

"Does the grid beat doing nothing?" Design-Bench convention demands this baseline and the
paper reports none. Writes results/dobest.json. Noiseless oracle per mbo.eval_designs.
"""
import json
import os

import numpy as np
import mbo

HERE = os.path.dirname(os.path.abspath(__file__))
CAMERA = os.path.join(HERE, '..', 'results', 'results_camera.json')
OUT = os.path.join(HERE, '..', 'results', 'dobest.json')
CELLS = [f'{s}:{o}' for s in ('ens', 'botorchgp', 'svgp') for o in ('grad', 'perturb', 'cma')]


def main():
    cam = json.load(open(CAMERA))['mbo']
    R = {}
    print(f'{"task":16}{"data_best":>12}{"donoth_p100":>13}{"donoth_p50":>12}'
          f'{"best_cell":>11}{"cell":>18}{"/data":>8}{"/donoth":>9}')
    for T in mbo.ALL_TASKS:
        t = T()
        x, y = t.data()                      # y = noisy observed targets
        yo = t.oracle(x)                     # NOISELESS oracle over the dataset
        data_best = float(yo.max())
        top = np.argsort(y)[-mbo.TOP:]       # do-nothing: top-128 by observed noisy y
        dn = yo[top]
        dn_p100, dn_p50 = float(dn.max()), float(np.median(dn))
        # best grid cell (on,on camera)
        cells = {c: cam[t.name][c]['p100']['mean'] for c in CELLS
                 if c in cam.get(t.name, {}) and isinstance(cam[t.name][c].get('p100'), dict)}
        best_cell = max(cells, key=cells.get) if cells else None
        best_p100 = cells[best_cell] if best_cell else float('nan')
        # NOTE: ratio is only meaningful when the base is POSITIVE; for negative scores a
        # smaller ratio can mean BETTER (both negative). gap = best - data is monotone-correct.
        r_data = best_p100 / data_best if data_best not in (0.0,) else float('nan')
        r_dn = best_p100 / dn_p100 if dn_p100 not in (0.0,) else float('nan')
        gap_data = best_p100 - data_best
        R[t.name] = dict(data_best=data_best, donothing_p100=dn_p100, donothing_p50=dn_p50,
                         best_cell=best_cell, best_cell_p100=best_p100,
                         gap_best_minus_data=gap_data,
                         ratio_best_over_data=r_data, ratio_best_over_donothing=r_dn,
                         ratio_note='ratio unreliable for negative base; use gap_best_minus_data',
                         beats_donothing=bool(best_p100 > dn_p100),
                         beats_data_best=bool(best_p100 > data_best))
        print(f'{t.name:16}{data_best:12.3f}{dn_p100:13.3f}{dn_p50:12.3f}'
              f'{best_p100:11.3f}{str(best_cell):>18}{r_data:8.2f}{r_dn:9.2f}')
    n_beat_dn = sum(v['beats_donothing'] for v in R.values())
    n_beat_data = sum(v['beats_data_best'] for v in R.values())
    print(f'\nbeats do-nothing top-128: {n_beat_dn}/{len(R)} tasks | '
          f'beats absolute data-best: {n_beat_data}/{len(R)} tasks')
    json.dump({'note': 'best_cell from (on,on) camera; oracle noiseless; donothing=top-128 by noisy y',
               'per_task': R, 'n_beats_donothing': n_beat_dn, 'n_beats_data_best': n_beat_data,
               'n_tasks': len(R)}, open(OUT, 'w'), indent=1)
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
