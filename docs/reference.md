# Reference

## pll_standings

```python
pypll.pll_standings(year=2025, champ_series=True)
```

Fetch PLL team standings for a given season.

### Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2025` | Season year. Data is only available during or after the season has begun. |
| `champ_series` | `bool` | `True` | `True` for championship series standings, `False` for regular season standings. |

### Returns

`pd.DataFrame` — one row per team.

### Columns

| Column | Type | Description |
|---|---|---|
| `teamId` | str | Unique team identifier |
| `fullName` | str | Full team name (e.g. "Atlas LC") |
| `location` | str | Team city/location |
| `locationCode` | str | Short location code |
| `urlLogo` | str | URL to the team logo image |
| `seed` | int | Playoff seeding position |
| `wins` | int | Total wins |
| `losses` | int | Total losses |
| `ties` | int | Total ties |
| `scores` | int | Total goals scored |
| `scoresAgainst` | int | Total goals allowed |
| `scoreDiff` | int | Goal differential (scores - scoresAgainst) |
| `conferenceWins` | int | Wins within conference |
| `conferenceLosses` | int | Losses within conference |
| `conferenceTies` | int | Ties within conference |
| `conferenceScores` | int | Goals scored in conference games |
| `conferenceScoresAgainst` | int | Goals allowed in conference games |
| `conference` | str | Conference name |
| `conferenceSeed` | int | Seeding within conference |

### Example

```python
import pypll

df = pypll.pll_standings(year=2025)
print(df[["fullName", "wins", "losses", "scoreDiff"]])
#       fullName  wins  losses  scoreDiff
# 0     Atlas LC     8       2         15
# 1    Chrome LC     7       3         12
```

---

## pll_player_stats

```python
pypll.pll_player_stats(year=2025, season_segment="champseries")
```

Fetch PLL player season statistics.

### Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2025` | Season year. Data is only available during or after the season has begun. |
| `season_segment` | `str` | `"champseries"` | Portion of the season: `"champseries"` for championship series (playoffs) or `"regular"` for regular season. |

### Returns

`pd.DataFrame` — one row per player, approximately 70 columns.

### Columns

**Player identity fields:**

| Column | Type | Description |
|---|---|---|
| `officialId` | str | Unique player identifier |
| `firstName` | str | Player's first name |
| `lastName` | str | Player's last name |
| `slug` | str | URL slug |
| `profileUrl` | str | URL to the player profile page |
| `jerseyNum` | str | Jersey number |
| `position` | str | Position code (e.g. "A", "M", "D", "G") |
| `positionName` | str | Full position name |
| `experience` | int | Years of professional experience |

**Team fields** (prefixed with `team_`):

`team_teamId`, `team_fullName`, `team_location`, and other team attributes.

**Stat fields** (50+ columns inlined at top level):

Includes `goals`, `assists`, `shots`, `groundBalls`, `causedTurnovers`, `faceoffWins`, `saves`, and more. The exact set of columns varies by season.

### Example

```python
import pypll

df = pypll.pll_player_stats(year=2025, season_segment="champseries")
print(df[["firstName", "lastName", "position", "goals", "assists"]].head())
#   firstName  lastName position  goals  assists
# 0      Lyle  Thompson        A     42       31
# 1     Myles     Jones        A     38       27
```

---

## pll_events

```python
pypll.pll_events(year=2025, include_cs=True, include_wll=True)
```

Fetch PLL game schedule and results for a given season.

### Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2025` | Season year. |
| `include_cs` | `bool` | `True` | When `True`, includes championship series (playoff) games. |
| `include_wll` | `bool` | `True` | When `True`, includes Women's Lacrosse League (WLL) games. |

### Returns

`pd.DataFrame` — one row per game event.

### Columns

**Top-level event fields:**

| Column | Type | Description |
|---|---|---|
| `eventId` | str | Unique game identifier |
| `startTime` | str | ISO 8601 start datetime in UTC |
| `status` | str | Game status (e.g. "final", "scheduled") |
| `homeScore` | int | Home team final score (None if not yet played) |
| `awayScore` | int | Away team final score (None if not yet played) |
| `venue` | str | Stadium/venue name |
| `broadcaster` | str | TV/streaming broadcaster |
| `league` | str | League identifier (e.g. "PLL", "WLL") |

**Home team fields** (prefixed with `home_`):

`home_teamId`, `home_fullName`, `home_location`, `home_urlLogo`, and other home team attributes.

**Away team fields** (prefixed with `away_`):

`away_teamId`, `away_fullName`, `away_location`, `away_urlLogo`, and other away team attributes.

### Example

```python
import pypll

df = pypll.pll_events(year=2025, include_cs=True, include_wll=False)
print(df[["startTime", "home_fullName", "away_fullName", "homeScore", "awayScore"]].head())
#               startTime home_fullName away_fullName  homeScore  awayScore
# 0  2025-06-01T17:00:00Z      Atlas LC     Chrome LC       12.0       10.0
```

---

## pll_draft_order

```python
pypll.pll_draft_order(year=2025, league="PLL")
```

Fetch the official draft order for a given year.

### Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2025` | Draft year. Data is only available once the draft has occurred. |
| `league` | `str` | `"PLL"` | League identifier: `"PLL"` for the Premier Lacrosse League or `"WLL"` for the Women's Lacrosse League. |

### Returns

`pd.DataFrame` — one row per draft pick.

### Columns

| Column | Type | Description |
|---|---|---|
| `id` | str | Unique pick record identifier |
| `year` | int | Draft year |
| `round` | int | Draft round number |
| `roundPick` | int | Pick number within the round |
| `overallPick` | int | Overall pick number across all rounds |
| `teamId` | str | Team that holds the pick |
| `league` | str | League identifier |
| `pick_playerName` | str | Drafted player's full name (None if no player on record) |
| `pick_college` | str | Player's college (None if no player on record) |
| `pick_position` | str | Player's position (None if no player on record) |
| `pick_playerId` | str | Player's official ID (None if no player on record) |

### Example

```python
import pypll

df = pypll.pll_draft_order(year=2025, league="PLL")
print(df[["round", "overallPick", "teamId", "pick_playerName", "pick_position"]].head())
#    round  overallPick  teamId pick_playerName pick_position
# 0      1            1   ATLAS      John Smith             A
# 1      1            2  CHROME    Mike Johnson             M
```

---

## pll_draft_predictions

```python
pypll.pll_draft_predictions(year=2026)
```

Fetch PLL mock draft predictions from league analysts.

### Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2026` | Draft year. Predictions are typically published in the months leading up to the draft. |

### Returns

`pd.DataFrame` — one row per analyst prediction.

### Columns

| Column | Type | Description |
|---|---|---|
| `id` | str | Unique prediction record identifier |
| `year` | int | Draft year |
| `analystName` | str | Name of the analyst making the prediction |
| `playerName` | str | Predicted player name |
| `imageUrl` | str | URL to the player image |
| `position` | str | Player's position (e.g. "A", "M", "D", "G") |
| `college` | str | Player's college |
| `collegeLogo` | str | URL to the college logo |
| `overallRank` | int | Analyst's overall prospect ranking |
| `positionRank` | int | Ranking within the player's position group |
| `change` | int | Change in ranking from the previous update |
| `analysis` | str | Analyst's written scouting notes |
| `league` | str | League identifier |

### Example

```python
import pypll

df = pypll.pll_draft_predictions(year=2026)
print(df[["analystName", "playerName", "position", "overallRank", "college"]].head())
#     analystName    playerName position  overallRank  college
# 0  John Analyst  Connor Murphy        A            1      UNC
# 1  John Analyst    Tyler Davis        M            2  Maryland
```

---

## pll_free_agents

```python
pypll.pll_free_agents(year=2026)
```

Fetch PLL free agent signings and available players for a given year. This function queries the PLL GraphQL API. Data is available once free agency has opened for the specified year.

### Parameters

| Name | Type | Default | Description |
|---|---|---|---|
| `year` | `int` | `2026` | Free agency year. |

### Returns

`pd.DataFrame` — one row per free agent.

### Columns

**Player fields:**

| Column | Type | Description |
|---|---|---|
| `name` | str | Player's full name |
| `firstName` | str | Player's first name |
| `lastName` | str | Player's last name |
| `slug` | str | URL slug |
| `profileUrl` | str | URL to the player profile page |
| `age` | int | Player's age |
| `experience` | int | Years of professional experience |
| `position` | str | Position code (e.g. "A", "M", "D", "G") |
| `status` | str | Player status |

**Transaction fields:**

| Column | Type | Description |
|---|---|---|
| `officialId` | str | Unique player identifier |
| `newContractStatus` | str | Contract status (e.g. "signed", "unsigned") |
| `newTeamId` | str | Team the player signed with (None if unsigned) |
| `prevTeamId` | str | Team the player was previously on |
| `thirtyPercentThresholdMet` | bool | Whether the 30% salary threshold was met |

### Example

```python
import pypll

df = pypll.pll_free_agents(year=2026)
print(df[["name", "position", "prevTeamId", "newTeamId", "newContractStatus"]].head())
#             name position prevTeamId newTeamId newContractStatus
# 0  Connor Martin        A      ATLAS    CHROME            signed
# 1  Kyle Hartzell        D     CHROME      None          unsigned
```
