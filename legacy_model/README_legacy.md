# Momentum Overlay (legacy desktop model)

What the desk told us:

- Runs on the desk PC through Windows Task Scheduler (`run_momentum.bat`), on the first weekday of each month at 08:30 Amsterdam time.
- Reads `C:\Desk\exports\prices_export.csv`, a nightly export from an old Eikon macro (split-adjusted history, last trade and official close).
- Writes `target_weights_YYYY-MM.csv` (ric, score, weight). The PM uses these weights.
- `legacy_output/` holds the files the PC produced for March to September 2026. These are the reference for your shadow run.
- The export file itself is gone (the macro was switched off). You will have to rebuild the inputs from the platform.
