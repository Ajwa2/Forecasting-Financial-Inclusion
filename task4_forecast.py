"""Task 4: Forecast Account Ownership (Access) and Digital Payment Usage (2025-2027).

This script:
- loads the unified enriched Excel in `data/processed`
- extracts 'Account Ownership Rate' (Global Findex) and a proxy for digital payments
- fits a linear trend and a logit-trend (bounded) model for each series
- forecasts 2025-2027: baseline (trend), event-augmented (NFIS target interpolation),
  and three scenarios (optimistic/base/pessimistic)
- writes results to `reports/forecasts_task4.csv` and prints a short summary.

Limitations are explicitly noted in the printed summary.
"""

from pathlib import Path
import numpy as np
import pandas as pd


def safe_logit(p, eps=1e-6):
    p = np.clip(p, eps, 1 - eps)
    return np.log(p / (1 - p))


def safe_inv_logit(x):
    return 1 / (1 + np.exp(-x))


def fit_linear(years, y):
    X = np.vstack([np.ones_like(years), years]).T
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    y_hat = X.dot(beta)
    resid = y - y_hat
    s2 = (resid ** 2).sum() / max(1, (len(y) - X.shape[1]))
    XtX_inv = np.linalg.pinv(X.T.dot(X))
    return {'beta': beta, 's2': s2, 'XtX_inv': XtX_inv}


def predict_linear(model, years_pred):
    Xp = np.vstack([np.ones_like(years_pred), years_pred]).T
    y_pred = Xp.dot(model['beta'])
    # prediction se: sqrt(s2 * (1 + x0' (X'X)^{-1} x0))
    se = np.sqrt(np.array([model['s2'] * (1 + x.dot(model['XtX_inv']).dot(x)) for x in Xp]))
    return y_pred, se


def fit_logit_linear(years, y_pct):
    # y_pct in percent (0-100) -> p in (0,1)
    p = np.clip(y_pct / 100.0, 1e-6, 1 - 1e-6)
    z = safe_logit(p)
    return fit_linear(years, z)


def predict_logit_linear(model, years_pred):
    z_pred, se_z = predict_linear(model, years_pred)
    p_pred = safe_inv_logit(z_pred)
    # approximate se on probability via delta method: se_p = se_z * p*(1-p)
    se_p = se_z * (p_pred * (1 - p_pred))
    return p_pred * 100.0, se_p * 100.0


def load_series(path):
    df = pd.read_excel(path, sheet_name='ethiopia_fi_unified_data')
    return df


def select_findex(df, indicator_name):
    # prefer Global Findex source entries
    sub = df[df['indicator'] == indicator_name]
    g = sub[sub['source_name'].str.contains('Global Findex', na=False)]
    if not g.empty:
        sel = g.copy()
    else:
        sel = sub.copy()
    # pick the most relevant numeric value per fiscal_year by taking the max
    sel = sel.dropna(subset=['fiscal_year'])
    sel = sel.groupby('fiscal_year', as_index=False).agg({'value_numeric': 'max'})
    sel = sel.sort_values('fiscal_year')
    return sel['fiscal_year'].astype(int).values, sel['value_numeric'].values


def main():
    root = Path('data/processed')
    path = root / 'ethiopia_fi_unified_data_enriched.xlsx'
    if not path.exists():
        raise FileNotFoundError(path)

    df = load_series(path)

    # --- Account Ownership (Access) ---
    years_acc, vals_acc = select_findex(df, 'Account Ownership Rate')

    # remove NFIS target rows (source not Global Findex) if present
    mask_history = years_acc <= 2024
    years_acc = years_acc[mask_history]
    vals_acc = vals_acc[mask_history]

    # Fit models
    lin_acc = fit_linear(years_acc, vals_acc)
    logit_acc = fit_logit_linear(years_acc, vals_acc)

    years_fore = np.array([2025, 2026, 2027])

    y_lin_pred, se_lin = predict_linear(lin_acc, years_fore)
    y_logit_pred, se_logit = predict_logit_linear(logit_acc, years_fore)

    # Choose baseline = logit (bounded) for Access
    baseline_acc = y_logit_pred
    baseline_se_acc = se_logit

    # Event-augmented: use NFIS-II target if present in dataset as an upper-bound path
    nfis = df[(df['indicator'] == 'Account Ownership Rate') & (df['source_name'].str.contains('NFIS', na=False))]
    event_acc = None
    if not nfis.empty:
        # take numeric target if exists (e.g., 70 in 2025), interpolate from last observed 2024
        target_row = nfis.sort_values('fiscal_year').iloc[-1]
        target_year = int(target_row['fiscal_year'])
        target_val = float(target_row['value_numeric'])
        last_year = max(years_acc)
        last_val = float(vals_acc[years_acc.argmax()])
        # linear interpolation from last_year->target_year, and extend to 2027
        interp_years = np.concatenate(([last_year], years_fore, [target_year]))
        # create simple linear path from last_val to target
        def event_path(y):
            if y <= last_year:
                return last_val
            elif y >= target_year:
                return target_val
            else:
                frac = (y - last_year) / (target_year - last_year)
                return last_val + frac * (target_val - last_val)

        event_acc = np.array([event_path(y) for y in years_fore])

    # Scenario bands (optimistic/base/pessimistic) around baseline using baseline_se_acc
    opt_acc = baseline_acc + 1.5 * baseline_se_acc
    base_acc = baseline_acc
    pess_acc = baseline_acc - 1.5 * baseline_se_acc

    # --- Digital Payment Usage ---
    # Proxy: Mobile Money Account Rate (Global Findex) and fallback to Mobile Money Activity Rate
    years_mm, vals_mm = select_findex(df, 'Mobile Money Account Rate')
    if len(years_mm) == 0:
        years_mm, vals_mm = select_findex(df, 'Mobile Money Activity Rate')

    # Fit same models for digital proxy
    lin_mm = fit_linear(years_mm, vals_mm)
    logit_mm = fit_logit_linear(years_mm, vals_mm)
    y_lin_mm, se_lin_mm = predict_linear(lin_mm, years_fore)
    y_logit_mm, se_logit_mm = predict_logit_linear(logit_mm, years_fore)
    baseline_mm = y_logit_mm
    baseline_se_mm = se_logit_mm

    # Event-augmented for digital payments: if Fayda Digital ID or Payment system launch exists, create modest lift
    ev = df[df['indicator'].str.contains('Fayda|Instant Payment System|QR Code', na=False)]
    event_mm = None
    if not ev.empty:
        # modest +5 percentage points in 2025, +3 in 2026, +2 in 2027
        event_mm = baseline_mm + np.array([5.0, 3.0, 2.0])

    opt_mm = baseline_mm + 1.5 * baseline_se_mm
    base_mm = baseline_mm
    pess_mm = baseline_mm - 1.5 * baseline_se_mm

    # collate results
    rows = []
    for i, y in enumerate(years_fore):
        rows.append({'series': 'Account Ownership Rate', 'year': int(y), 'baseline': float(base_acc[i]),
                     'ci95_low': float(base_acc[i] - 1.96 * baseline_se_acc[i]),
                     'ci95_high': float(base_acc[i] + 1.96 * baseline_se_acc[i]),
                     'optimistic': float(opt_acc[i]), 'pessimistic': float(pess_acc[i]),
                     'event_augmented': float(event_acc[i]) if event_acc is not None else None})
        rows.append({'series': 'Digital Payment Usage (proxy)', 'year': int(y), 'baseline': float(base_mm[i]),
                     'ci95_low': float(base_mm[i] - 1.96 * baseline_se_mm[i]),
                     'ci95_high': float(base_mm[i] + 1.96 * baseline_se_mm[i]),
                     'optimistic': float(opt_mm[i]), 'pessimistic': float(pess_mm[i]),
                     'event_augmented': float(event_mm[i]) if event_mm is not None else None})

    out = pd.DataFrame(rows)
    outdir = Path('reports')
    outdir.mkdir(parents=True, exist_ok=True)
    out.to_csv(outdir / 'forecasts_task4.csv', index=False)

    # Print concise summary
    print('\nForecast summary (2025-2027) written to reports/forecasts_task4.csv')
    print('\nKey choices:')
    print('- Access series: `Account Ownership Rate` (Global Findex historical points used: {})'.format(list(years_acc)))
    print('- Digital series: proxy used = `Mobile Money Account Rate` (Findex)')
    print('\nBaseline model: logit-transformed linear trend (bounded 0-100).')
    print('Event-augmented paths: NFIS-II target used for Access when available; payment system / digital ID events used for digital proxy.')
    print('\nLimitations: sparse historical points (4 Findex obs), heterogeneous sources, and proxy usage for digital payments. Treat numeric forecasts as indicative ranges, not precise predictions.')


if __name__ == '__main__':
    main()
