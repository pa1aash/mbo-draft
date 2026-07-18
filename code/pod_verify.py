"""Phase 2 reproduction gate, pod edition.

Compares a POD-generated off_off grid (results/corners/pod_off_off.json) to:
  (A) results/results_camera.json cell-by-cell  -- the camera IS the off_off engine
      (ens:cma Branin = -14.010635042190552), so a faithful pod reproduces it near-exactly;
  (B) the published Table 1 via analyze_corners.reproduction_check (its pre-stated tolerance);
  (C) eta2 (surr/opt/inter) and the Friedman omnibus, vs published 0.37/0.01/0.17, 6.1e-5.

TOLERANCES, stated BEFORE the look (synthetic is claimed platform-invariant; macOS matched
the camera to 12 decimals):
  (A) PASS if max |pod_mean - camera_mean| over all 63 grid cells < 1e-3, AND
      |ens:cma Branin mean - (-14.010635042190552)| < 1e-4.
  (B) analyze_corners pre-stated: per-cell |diff|<=max(2*SEM,0.10*|pub|) if |pub|>1 else 0.10;
      PASS if >=90% (>=57/63) cells within tolerance.
  (C) |eta2_surr - 0.367| <= 0.005 ; |eta2_opt - 0.01| <= 0.02 ; |eta2_inter - 0.17| <= 0.02 ;
      Friedman p in [3e-5, 1.2e-4] (within ~2x of 6.09e-5).
Overall PASS requires A and B and C. A material synthetic divergence => STOP (Phase 2.2).
"""
import json
import os
import sys

import numpy as np

import analyze_corners as AC

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'results')
POD = os.path.join(RES, 'corners', 'pod_off_off.json')
CAMERA = os.path.join(RES, 'results_camera.json')


def camera_compare(pod_means):
    cam = json.load(open(CAMERA))['mbo']
    diffs = []
    worst = None
    for c in AC.CELLS:
        for j, t in enumerate(AC.TASKS):
            got = pod_means[c][j]
            camv = cam.get(t, {}).get(c, {}).get('p100')
            if got is None or not isinstance(camv, dict):
                continue
            d = abs(got - camv['mean'])
            diffs.append(d)
            if worst is None or d > worst[0]:
                worst = (d, c, t, got, camv['mean'])
    branin = cam['Branin-2D']['ens:cma']['p100']['mean']
    pod_branin = pod_means['ens:cma'][AC.TASKS.index('Branin-2D')]
    return dict(max_abs_diff=float(max(diffs)) if diffs else None,
                n_cells=len(diffs),
                worst=dict(diff=worst[0], cell=worst[1], task=worst[2],
                           pod=worst[3], camera=worst[4]) if worst else None,
                 enscma_branin_pod=float(pod_branin),
                enscma_branin_camera=float(branin),
                enscma_branin_diff=float(abs(pod_branin - branin)))


def main():
    if not os.path.exists(POD):
        print(f'MISSING {POD} -- run the off_off grid first', file=sys.stderr)
        sys.exit(1)
    done, ncell = AC.is_complete(POD)
    means = AC.grid_means(POD)
    allv = AC.grid_all(POD)

    cam = camera_compare(means)
    rows, npass, ntot = AC.reproduction_check(means, allv)
    e = AC.eta2_from_means(means)
    rf = AC.ranks_and_friedman(means)

    A_ok = (cam['max_abs_diff'] is not None and cam['max_abs_diff'] < 1e-3
            and cam['enscma_branin_diff'] < 1e-4)
    B_ok = npass >= 0.90 * ntot
    C_ok = (abs(e['surr'] - 0.367) <= 0.005 and abs(e['opt'] - 0.01) <= 0.02
            and abs(e['inter'] - 0.17) <= 0.02
            and 3e-5 <= rf['friedman_p'] <= 1.2e-4)
    verdict = 'PASS' if (done and A_ok and B_ok and C_ok) else 'FAIL'

    report = dict(
        complete=bool(done), cells_present=ncell,
        camera_compare=cam, camera_ok=bool(A_ok),
        published_cells_within_tol=npass, published_cells_total=ntot, published_ok=bool(B_ok),
        eta2=e, friedman_p=rf['friedman_p'], eta2_friedman_ok=bool(C_ok),
        verdict=verdict)
    json.dump(report, open(os.path.join(RES, 'corners', 'pod_verification.json'), 'w'),
              indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))

    print('=== POD REPRODUCTION GATE ===')
    print(f'complete: {done} ({ncell}/63 cells @30 seeds)')
    print(f'(A) camera: max|diff|={cam["max_abs_diff"]:.3e} worst={cam["worst"]}')
    print(f'    ens:cma Branin pod={cam["enscma_branin_pod"]:.12f} '
          f'camera={cam["enscma_branin_camera"]:.12f} diff={cam["enscma_branin_diff"]:.3e} -> {A_ok}')
    print(f'(B) published: {npass}/{ntot} cells within tol -> {B_ok}')
    print(f'(C) eta2 surr={e["surr"]:.4f} opt={e["opt"]:.4f} inter={e["inter"]:.4f} '
          f'Friedman p={rf["friedman_p"]:.3e} -> {C_ok}')
    print(f'VERDICT: {verdict}')


if __name__ == '__main__':
    main()
