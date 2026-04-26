# F1 Telemetry Analysis

A multi-file Python project analysing real Formula 1 race data using the FastF1 API.

## Files

### analysis.py — 2024 British Grand Prix
Analyses lap time progression, fastest lap speed trace, and tyre strategy for Verstappen, Hamilton, and Norris.

### analysis_2026_japan.py — 2026 Japanese Grand Prix
Analyses lap time progression, fastest lap speed trace, and tyre strategy for Antonelli, Piastri, and Leclerc.

### team_analysis_2026.py — 2026 Season Team Comparison
Compares Mercedes, Ferrari, and McLaren across the first three races of 2026 (Australia, China, Japan).
- Average race pace per team per circuit
- Fastest lap trends per driver across all three races
- Tyre strategy breakdown for the Japanese GP

## Charts generated
| File | Description |
|---|---|
| lap_time_progression.png | 2024 British GP lap times — VER, HAM, NOR |
| speed_trace.png | 2024 British GP fastest lap speed trace |
| tyre_strategy.png | 2024 British GP tyre strategy |
| japan_2026_lap_times.png | 2026 Japanese GP lap times — ANT, PIA, LEC |
| japan_2026_speed_trace.png | 2026 Japanese GP speed trace |
| japan_2026_tyre_strategy.png | 2026 Japanese GP tyre strategy |
| team_avg_pace_2026.png | 2026 average race pace by team |
| driver_fastest_laps_2026.png | 2026 fastest lap trends per driver |
| japan_tyre_strategy_teams_2026.png | 2026 Japanese GP tyre strategy — 6 drivers |

## Tech stack
- Python 3.13
- FastF1 (F1 timing and telemetry data)
- NumPy (data processing)
- Matplotlib (visualisation)

## How to run
```
pip install fastf1 matplotlib numpy
python analysis.py
python analysis_2026_japan.py
python team_analysis_2026.py
```