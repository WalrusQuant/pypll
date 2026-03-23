# Getting Started

## Installation

### From GitHub

`pypll` is not yet published to PyPI. Install the latest version directly from GitHub:

```bash
pip install git+https://github.com/WalrusQuant/pypll.git
```

### From a local clone

```bash
git clone https://github.com/WalrusQuant/pypll.git
cd pypll
pip install -e .
```

## Dependencies

- [requests](https://docs.python-requests.org/) — HTTP client for API calls
- [pandas](https://pandas.pydata.org/) — all functions return DataFrames

Both are installed automatically with `pypll`.

## Quick start

```python
import pypll
```

### Standings

```python
standings = pypll.pll_standings(year=2025)
print(standings[["fullName", "wins", "losses", "scoreDiff"]])
```

### Player stats

```python
# Championship series stats
stats = pypll.pll_player_stats(year=2025, season_segment="champseries")
print(stats[["firstName", "lastName", "position", "goals", "assists"]].head())

# Regular season stats
reg_stats = pypll.pll_player_stats(year=2025, season_segment="regular")
```

### Game schedule and results

```python
# PLL games only (no WLL)
events = pypll.pll_events(year=2025, include_cs=True, include_wll=False)
print(events[["startTime", "home_fullName", "away_fullName", "homeScore", "awayScore"]].head())
```

### Draft order

```python
# Official draft picks
draft = pypll.pll_draft_order(year=2025, league="PLL")
print(draft[["round", "overallPick", "teamId", "pick_playerName", "pick_position"]].head())

# WLL draft
wll_draft = pypll.pll_draft_order(year=2025, league="WLL")
```

### Mock draft predictions

```python
predictions = pypll.pll_draft_predictions(year=2026)
print(predictions[["analystName", "playerName", "position", "overallRank", "college"]].head())
```

### Free agents

```python
free_agents = pypll.pll_free_agents(year=2026)
print(free_agents[["name", "position", "prevTeamId", "newTeamId", "newContractStatus"]].head())
```

## Data availability

Season data (standings, player stats, events) is only available **during or after** the relevant season has begun. Querying a future year or a year before the season starts will return an empty DataFrame or raise a `RuntimeError`.

Draft order data is available once the draft has taken place. Mock draft predictions are typically published in the months leading up to the draft. Free agent data becomes available once the free agency period opens.
