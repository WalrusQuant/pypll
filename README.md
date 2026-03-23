# pypll

A Python client for the Premier Lacrosse League stats API. All functions return [pandas](https://pandas.pydata.org/) DataFrames.

## Installation

```bash
pip install pypll
```

For a development install from source:

```bash
pip install -e .
```

## Quick Start

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

# Official draft order
draft = pypll.pll_draft_order(year=2025, league="PLL")
print(draft[["round", "overallPick", "teamId", "pick_playerName"]].head())

# Mock draft predictions from analysts
predictions = pypll.pll_draft_predictions(year=2026)
print(predictions[["analystName", "playerName", "position", "overallRank"]].head())

# Free agent signings
free_agents = pypll.pll_free_agents(year=2026)
print(free_agents[["name", "position", "prevTeamId", "newTeamId", "newContractStatus"]].head())
```

### Sample output

```
# pll_standings
        fullName  wins  losses  scoreDiff
0       Atlas LC     8       2         15
1      Chrome LC     7       3         12

# pll_player_stats
  firstName  lastName position  goals  assists
0      Lyle  Thompson        A     42       31
1     Myles     Jones        A     38       27

# pll_events
              startTime  home_fullName away_fullName  homeScore  awayScore
0  2025-06-01T17:00:00Z       Atlas LC     Chrome LC       12.0       10.0

# pll_draft_order
   round  overallPick   teamId pick_playerName pick_position
0      1            1    ATLAS      John Smith             A
1      1            2   CHROME    Mike Johnson             M

# pll_draft_predictions
    analystName   playerName position  overallRank  college
0  John Analyst  Connor Murphy        A            1     UNC

# pll_free_agents
            name position prevTeamId newTeamId newContractStatus
0  Connor Martin        A      ATLAS    CHROME            signed
```

---

## Function Reference

### `pll_standings(year=2025, champ_series=True)`

Fetch team standings.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2025` | Season year |
| `champ_series` | `bool` | `True` | `True` for championship series standings, `False` for regular season |

**Returns:** `pd.DataFrame` — one row per team.

Key columns: `teamId`, `fullName`, `location`, `wins`, `losses`, `ties`, `scores`, `scoresAgainst`, `scoreDiff`, `conference`, `conferenceSeed`, `seed`

---

### `pll_player_stats(year=2025, season_segment="champseries")`

Fetch player season statistics.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2025` | Season year |
| `season_segment` | `str` | `"champseries"` | Segment of the season: `"champseries"` (playoffs) or `"regular"` |

**Returns:** `pd.DataFrame` — one row per player, approximately 70 columns.

Column groups:
- **Player identity:** `officialId`, `firstName`, `lastName`, `slug`, `profileUrl`, `jerseyNum`, `position`, `positionName`, `experience`
- **Team info** (`team_` prefix): `team_teamId`, `team_fullName`, `team_location`, etc.
- **Stats** (50+ columns inlined): `goals`, `assists`, `shots`, `groundBalls`, `causedTurnovers`, `faceoffWins`, `saves`, and more

---

### `pll_events(year=2025, include_cs=True, include_wll=True)`

Fetch game schedule and results.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2025` | Season year |
| `include_cs` | `bool` | `True` | Include championship series (playoff) games |
| `include_wll` | `bool` | `True` | Include Women's Lacrosse League (WLL) games |

**Returns:** `pd.DataFrame` — one row per game event.

Key columns: `eventId`, `startTime`, `status`, `homeScore`, `awayScore`, `venue`, `broadcaster`, `league`, plus `home_*` and `away_*` prefixed team info columns.

---

### `pll_draft_order(year=2025, league="PLL")`

Fetch the official draft order.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2025` | Draft year |
| `league` | `str` | `"PLL"` | League identifier: `"PLL"` or `"WLL"` |

**Returns:** `pd.DataFrame` — one row per draft pick.

Key columns: `id`, `year`, `round`, `roundPick`, `overallPick`, `teamId`, `league`, plus `pick_playerName`, `pick_college`, `pick_position`, `pick_playerId` (all `None` if no player on record for that pick).

---

### `pll_draft_predictions(year=2026)`

Fetch mock draft predictions from PLL analysts.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2026` | Draft year |

**Returns:** `pd.DataFrame` — one row per analyst prediction.

Key columns: `analystName`, `playerName`, `position`, `college`, `overallRank`, `positionRank`, `change`, `analysis`, `league`

---

### `pll_free_agents(year=2026)`

Fetch free agent signings and available players.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2026` | Free agency year |

**Returns:** `pd.DataFrame` — one row per free agent.

Key columns: `name`, `firstName`, `lastName`, `position`, `age`, `experience`, `prevTeamId`, `newTeamId`, `newContractStatus`, `thirtyPercentThresholdMet`

---

## Data Availability

Season data (standings, player stats, events) is only available **during or after** the relevant season has begun. Querying a future year or a year before the season starts will return an empty DataFrame or raise a `RuntimeError`.

Draft order data is available once the draft has taken place. Mock draft predictions are typically published in the months leading up to the draft. Free agent data becomes available once the free agency period opens.

## License

MIT License. See [LICENSE](LICENSE) for details.
