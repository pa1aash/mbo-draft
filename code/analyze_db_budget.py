"""0C analysis -- DBM1/DBM2, per docs/PREREGISTRATION_V3.md section 0C.

Every estimator is IMPORTED from analyze_db.py rather than re-implemented, so the matched
numbers pass through the identical eta2 / Friedman / bootstrap code that produced the
published corner numbers. The only thing this module adds is the level axis and the
pre-registered decision rules.

Primary task set is the 7-task one (5 non-mujoco + Ant + DKitty), because the brief scopes
this arm to the FULL grid including MuJoCo and because docs/MUJOCO_CHECK.md's localization
argument lives there. The 5-task and GFP-dropped sets are reported alongside.

  python analyze_db_budget.py  -> results/db_budget/db_budget_analysis.json
"""
import json
import os

import numpy as np

import analyze_db as A

HERE = os.path.dirname(os.path.abspath(__file__))
DBB = os.path.join(HERE, '..', 'results', 'db_budget')
CORNERS = ['off_off', 'on_off', 'off_on', 'on_on']
LEVELS = ['native', 'up', 'down']
PRIMARY = 'up'
MUJOCO = ['AntMorphology', 'DKitty']
ETA2_FLOOR = 0.10          # DBM2 threshold
ALPHA = 0.05               # Friedman rejection level for "the rejecting corners"


def _load(tag, level, mujoco):
    p = os.path.join(DBB, f'corner_{tag}_{level}{"_mujoco_db" if mujoco else "_db"}.json')
    if not os.path.exists(p):
        return None, None
    R = json.load(open(p))
    return R.get('mbo', {}), R


def report(tag, level, taskset='7task'):
    d, R = _load(tag, level, False)
    if d is None:
        return {'status': 'MISSING'}
    tasks = [t for t in A.NONMUJOCO if not (taskset == 'noGFP' and t == 'GFP')]
    if taskset == '7task':
        dm, _ = _load(tag, level, True)
        if dm is None:
            return {'status': 'MISSING mujoco'}
        d = {**d, **dm}
        tasks = tasks + MUJOCO
    sv = A.seedvals(d, tasks)
    # A cell that ran for fewer seeds than its siblings means a MISSING run, and the
    # per-seed lists are then no longer index-aligned. Refuse rather than pair silently.
    ragged = {t: {c: len(v) for c, v in sv[t].items() if v}
              for t in tasks if len({len(v) for v in sv[t].values() if v}) > 1}
    if ragged:
        return {'status': f'RAGGED seed axis: {ragged}'}
    M, used = A.taskmeans(sv, tasks)
    if len(M) == 0:
        return {'status': 'NO COMPLETE TASKS'}
    e, f = A.eta2(M), A.friedman(M)
    return dict(status='ok', engine_meta=R.get('meta'), level_config=R.get('level_config'),
                achieved_q=R.get('achieved_q'), used_tasks=used, eta2=e, friedman=f,
                rejects=bool(f['friedman_p'] < ALPHA),
                opt_leader=max(e['opt_marg'], key=e['opt_marg'].get),
                opt_exceeds_surr=bool(e['opt'] > e['surr']),
                bootstrap=A.bootstrap(sv, tasks, B=10000,
                                      rng=np.random.default_rng(12345)))


def q_audit(rep):
    """Any corner whose PRIMARY level misses its target Q makes that corner's verdict
    UNVALIDATED rather than confirmed -- a budget-matching arm that did not match is not
    evidence about budget."""
    bad = {}
    for tag in CORNERS:
        r = rep['by_corner'].get(tag, {}).get(PRIMARY, {})
        qa = r.get('achieved_q') or {}
        off = {o: v for o, v in qa.items() if v.get('frac_cells_over_5pct', 0) > 0.05}
        if off:
            bad[tag] = off
    return bad


def main():
    rep = {'primary_level': PRIMARY, 'alpha': ALPHA, 'eta2_floor': ETA2_FLOOR,
           'by_corner': {}, 'secondary_tasksets': {}}
    for tag in CORNERS:
        rep['by_corner'][tag] = {lv: report(tag, lv) for lv in LEVELS}
    for ts in ('5task', 'noGFP'):
        rep['secondary_tasksets'][ts] = {
            tag: {lv: report(tag, lv, ts) for lv in LEVELS} for tag in CORNERS}

    ok = {tag: rep['by_corner'][tag][PRIMARY] for tag in CORNERS
          if rep['by_corner'][tag][PRIMARY].get('status') == 'ok'}
    missing = [t for t in CORNERS if t not in ok]
    rep['q_audit_failures'] = q_audit(rep)

    if missing:
        rep['DBM1'] = rep['DBM2'] = {'verdict': f'NOT EVALUATED — corners MISSING: {missing}'}
        rep['CALL'] = 'KEEP-PROVISIONAL — the matched grid is incomplete; no verdict is claimed'
        json.dump(rep, open(os.path.join(DBB, 'db_budget_analysis.json'), 'w'), indent=1,
                  default=lambda o: o.item() if hasattr(o, 'item') else str(o))
        print(rep['CALL'])
        return

    # ---- DBM1: does the optimizer-axis inversion survive matching? ----
    rejecting = [t for t, r in ok.items() if r['rejects']]
    leads = {t: ok[t]['opt_leader'] for t in rejecting}
    exceeds = {t: ok[t]['opt_exceeds_surr'] for t in rejecting}
    if not rejecting:
        v1 = ('DBM1 KILL FIRES — no corner rejects the Friedman omnibus under matched budget, '
              'so the inversion does not persist as a detectable effect. Per Agarwal (2021) '
              'non-rejection is not evidence of absence; the eta2 point estimates are reported '
              'and the frozen-cell explanation must be restated either way')
    elif all(leads[t] == 'perturb' for t in rejecting) and all(exceeds.values()):
        v1 = ('DBM1 CONFIRMED — in every corner that rejects under matched budget, '
              'perturbation still leads the optimizer marginal AND eta2_opt still exceeds '
              'eta2_surr; the inversion is not a budget artifact')
    else:
        bad_lead = [t for t in rejecting if leads[t] != 'perturb']
        bad_ex = [t for t in rejecting if not exceeds[t]]
        v1 = ('DBM1 KILL FIRES — matching collapses the inversion: '
              + (f'perturbation no longer leads in {bad_lead}; ' if bad_lead else '')
              + (f'eta2_opt no longer exceeds eta2_surr in {bad_ex}; ' if bad_ex else '')
              + 'the DB optimizer axis was in part a budget effect and the frozen-cell '
                'explanation must be restated')
    rep['DBM1'] = dict(rejecting_corners=rejecting, opt_leader=leads,
                       opt_exceeds_surr=exceeds, verdict=v1)

    # ---- DBM2: is the surrogate null a budget artifact? ----
    surr = {t: ok[t]['eta2']['surr'] for t in CORNERS}
    over = {t: v for t, v in surr.items() if v >= ETA2_FLOOR}
    v2 = (f'DBM2 CONFIRMED — eta2_surr stays below {ETA2_FLOOR} in all four corners under '
          f'matched budget ({ {t: round(v, 3) for t, v in surr.items()} }); the surrogate '
          f'null is not a budget artifact'
          if not over else
          f'DBM2 KILL FIRES — eta2_surr reaches {ETA2_FLOOR} or above in '
          f'{ {t: round(v, 3) for t, v in over.items()} }; the surrogate null does not '
          f'survive budget matching')
    rep['DBM2'] = dict(eta2_surr_by_corner=surr, over_floor=over, verdict=v2)

    # ---- the binary call ----
    ok1 = v1.startswith('DBM1 CONFIRMED')
    ok2 = v2.startswith('DBM2 CONFIRMED')
    qbad = bool(rep['q_audit_failures'])
    if ok1 and ok2 and not qbad:
        rep['CALL'] = ('PROMOTE — the inversion and the surrogate null both survive budget '
                       'matching on the full 7-task Design-Bench grid; section 6 can assert '
                       'rather than qualify')
    else:
        why = []
        if not ok1:
            why.append(v1.split(' — ')[0])
        if not ok2:
            why.append(v2.split(' — ')[0])
        if qbad:
            why.append(f'achieved-Q audit failed in {list(rep["q_audit_failures"])}')
        rep['CALL'] = ('KEEP-PROVISIONAL — ' + '; '.join(why)
                       + '. The optimizer half of section 6 keeps its qualifier.')

    json.dump(rep, open(os.path.join(DBB, 'db_budget_analysis.json'), 'w'), indent=1,
              default=lambda o: o.item() if hasattr(o, 'item') else str(o))

    print(f'=== DB budget-matched, primary level {PRIMARY}, 7-task ===')
    print(f'  {"corner":9} {"level":7} {"surr":>6} {"opt":>6} {"inter":>6} {"friedman":>9} '
          f'{"lead":>8} {"n":>3}')
    for tag in CORNERS:
        for lv in LEVELS:
            r = rep['by_corner'][tag][lv]
            if r.get('status') != 'ok':
                print(f'  {tag:9} {lv:7} {r.get("status")}')
                continue
            e, f = r['eta2'], r['friedman']
            print(f'  {tag:9} {lv:7} {e["surr"]:6.3f} {e["opt"]:6.3f} {e["inter"]:6.3f} '
                  f'{f["friedman_p"]:9.3e} {r["opt_leader"]:>8} {e["n_tasks"]:3d}')
    print()
    print(rep['DBM1']['verdict'])
    print(rep['DBM2']['verdict'])
    print()
    print(rep['CALL'])


if __name__ == '__main__':
    main()
