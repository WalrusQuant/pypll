# pypll

A Python client for the Premier Lacrosse League stats API. All functions return [pandas](https://pandas.pydata.org/) DataFrames.

## What it does

`pypll` wraps the PLL stats API and gives you clean DataFrames for standings, player statistics, game schedules, draft data, and free agency. No manual HTTP requests, no JSON parsing — just call a function and get a DataFrame back.

## Installation

`pypll` is not yet published to PyPI. Install directly from GitHub:

```bash
pip install git+https://github.com/WalrusQuant/pypll.git
```

## Quick example

```python
import pypll

# Team standings
standings = pypll.pll_standings(year=2025)
print(standings[["fullName", "wins", "losses", "scoreDiff"]])

# Player season stats (~70 columns)
stats = pypll.pll_player_stats(year=2025, season_segment="champseries")
print(stats[["firstName", "lastName", "position", "goals", "assists"]].head())

# Game schedule and results
events = pypll.pll_events(year=2025, include_cs=True, include_wll=False)
print(events[["startTime", "home_fullName", "away_fullName", "homeScore", "awayScore"]].head())
```

## Next steps

- [Getting Started](getting-started.md) — installation options and a walkthrough of every function
- [Reference](reference.md) — full parameter and column documentation for all six functions
