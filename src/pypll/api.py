"""Public functions for the PLL stats API."""

from __future__ import annotations

import pandas as pd

from ._client import _graphql_query, _rest_get

_FREE_AGENTS_QUERY = """
query($year: Int!) {
  freeAgents(year: $year) {
    player {
      name
      firstName
      lastName
      slug
      profileUrl
      age
      experience
      position
      status
    }
    officialId
    newContractStatus
    newTeamId
    prevTeamId
    thirtyPercentThresholdMet
  }
}
"""


def pll_standings(year: int = 2025, champ_series: bool = True) -> pd.DataFrame:
    """Fetch PLL team standings for a given season.

    Parameters
    ----------
    year : int, default 2025
        The season year to retrieve standings for. Data is only available
        during or after the season has begun.
    champ_series : bool, default True
        When True, returns championship series standings. When False, returns
        regular season standings.

    Returns
    -------
    pd.DataFrame
        One row per team with the following columns:

        - ``teamId`` : str — unique team identifier
        - ``fullName`` : str — full team name (e.g. "Atlas LC")
        - ``location`` : str — team city/location
        - ``locationCode`` : str — short location code
        - ``urlLogo`` : str — URL to the team logo image
        - ``seed`` : int — playoff seeding position
        - ``wins`` : int — total wins
        - ``losses`` : int — total losses
        - ``ties`` : int — total ties
        - ``scores`` : int — total goals scored
        - ``scoresAgainst`` : int — total goals allowed
        - ``scoreDiff`` : int — goal differential (scores - scoresAgainst)
        - ``conferenceWins`` : int — wins within conference
        - ``conferenceLosses`` : int — losses within conference
        - ``conferenceTies`` : int — ties within conference
        - ``conferenceScores`` : int — goals scored in conference games
        - ``conferenceScoresAgainst`` : int — goals allowed in conference games
        - ``conference`` : str — conference name
        - ``conferenceSeed`` : int — seeding within conference

    Examples
    --------
    >>> import pypll
    >>> df = pypll.pll_standings(year=2025)
    >>> df[["fullName", "wins", "losses", "scoreDiff"]].head()
          fullName  wins  losses  scoreDiff
    0     Atlas LC     8       2         15
    1  Chrome LC       7       3         12
    """
    params = {
        "year": year,
        "champSeries": "true" if champ_series else "false",
    }
    response = _rest_get("/standings", params=params)
    items = response["data"]["items"]
    return pd.DataFrame(items)


def pll_player_stats(
    year: int = 2025, season_segment: str = "champseries"
) -> pd.DataFrame:
    """Fetch PLL player season statistics.

    Parameters
    ----------
    year : int, default 2025
        The season year to retrieve stats for. Data is only available
        during or after the season has begun.
    season_segment : str, default "champseries"
        The portion of the season to retrieve. Common values:

        - ``"champseries"`` — championship series (playoff) stats
        - ``"regular"`` — regular season stats

    Returns
    -------
    pd.DataFrame
        One row per player. The DataFrame contains approximately 70 columns:

        Player identity fields:

        - ``officialId`` : str — unique player identifier
        - ``firstName`` / ``lastName`` : str — player name
        - ``slug`` : str — URL slug
        - ``profileUrl`` : str — URL to the player profile page
        - ``jerseyNum`` : str — jersey number
        - ``position`` : str — position code (e.g. "A", "M", "D", "G")
        - ``positionName`` : str — full position name
        - ``experience`` : int — years of professional experience

        Team fields (``team_`` prefix):

        - ``team_teamId``, ``team_fullName``, ``team_location``, etc.

        Stat fields (50+ columns inlined at top level), including goals, assists,
        shots, groundBalls, causedTurnovers, faceoffWins, saves, and more.

    Examples
    --------
    >>> import pypll
    >>> df = pypll.pll_player_stats(year=2025, season_segment="champseries")
    >>> df[["firstName", "lastName", "position", "goals", "assists"]].head()
      firstName  lastName position  goals  assists
    0     Lyle  Thompson        A     42       31
    1    Myles   Jones          A     38       27
    """
    params = {"year": year, "seasonSegment": season_segment}
    response = _rest_get("/players/season-stats", params=params)
    items = response["data"]["items"]

    rows = []
    for item in items:
        row: dict = {}

        # Top-level player fields
        top_level_keys = (
            "officialId",
            "firstName",
            "lastName",
            "slug",
            "profileUrl",
            "jerseyNum",
            "position",
            "positionName",
            "experience",
        )
        for key in top_level_keys:
            row[key] = item.get(key)

        # Nested team dict — prefix with team_
        team = item.get("team") or {}
        for key, value in team.items():
            row[f"team_{key}"] = value

        # Nested stats dict — inline at top level
        stats = item.get("stats") or {}
        for key, value in stats.items():
            row[key] = value

        rows.append(row)

    return pd.DataFrame(rows)


def pll_events(
    year: int = 2025, include_cs: bool = True, include_wll: bool = True
) -> pd.DataFrame:
    """Fetch PLL game schedule and results for a given season.

    Parameters
    ----------
    year : int, default 2025
        The season year to retrieve events for.
    include_cs : bool, default True
        When True, includes championship series (playoff) games.
    include_wll : bool, default True
        When True, includes Women's Lacrosse League (WLL) games.

    Returns
    -------
    pd.DataFrame
        One row per game event. Columns include:

        Top-level event fields:

        - ``eventId`` : str — unique game identifier
        - ``startTime`` : str — ISO 8601 start datetime (UTC)
        - ``status`` : str — game status (e.g. "final", "scheduled")
        - ``homeScore`` / ``awayScore`` : int — final scores (None if not played)
        - ``venue`` : str — stadium/venue name
        - ``broadcaster`` : str — TV/streaming broadcaster
        - ``league`` : str — league identifier (e.g. "PLL", "WLL")

        Home team fields (``home_`` prefix):

        - ``home_teamId``, ``home_fullName``, ``home_location``, ``home_urlLogo``, etc.

        Away team fields (``away_`` prefix):

        - ``away_teamId``, ``away_fullName``, ``away_location``, ``away_urlLogo``, etc.

    Examples
    --------
    >>> import pypll
    >>> df = pypll.pll_events(year=2025, include_cs=True, include_wll=False)
    >>> df[["startTime", "home_fullName", "away_fullName", "homeScore", "awayScore"]].head()
                  startTime  home_fullName away_fullName  homeScore  awayScore
    0  2025-06-01T17:00:00Z       Atlas LC     Chrome LC       12.0       10.0
    """
    params = {
        "year": year,
        "includeCS": "true" if include_cs else "false",
        "includeWLL": "true" if include_wll else "false",
    }
    response = _rest_get("/events", params=params)
    items = response["data"]["items"]

    rows = []
    for item in items:
        row: dict = {}

        # Top-level event fields (everything that is not a nested dict/list)
        for key, value in item.items():
            if key in ("homeTeam", "awayTeam"):
                continue
            if not isinstance(value, (dict, list)):
                row[key] = value

        # Nested home team — prefix with home_
        home = item.get("homeTeam") or {}
        for key, value in home.items():
            row[f"home_{key}"] = value

        # Nested away team — prefix with away_
        away = item.get("awayTeam") or {}
        for key, value in away.items():
            row[f"away_{key}"] = value

        rows.append(row)

    return pd.DataFrame(rows)


def pll_draft_order(year: int = 2025, league: str = "PLL") -> pd.DataFrame:
    """Fetch the official draft order for a given year.

    Parameters
    ----------
    year : int, default 2025
        The draft year. Data is only available once the draft has occurred.
    league : str, default "PLL"
        The league to retrieve draft data for. Use ``"PLL"`` for the Premier
        Lacrosse League or ``"WLL"`` for the Women's Lacrosse League.

    Returns
    -------
    pd.DataFrame
        One row per draft pick with the following columns:

        - ``id`` : str — unique pick record identifier
        - ``year`` : int — draft year
        - ``round`` : int — draft round number
        - ``roundPick`` : int — pick number within the round
        - ``overallPick`` : int — overall pick number across all rounds
        - ``teamId`` : str — team that holds the pick
        - ``league`` : str — league identifier

        Player fields (``pick_`` prefix, ``None`` if no player on record):

        - ``pick_playerName`` : str — drafted player's full name
        - ``pick_college`` : str — player's college
        - ``pick_position`` : str — player's position
        - ``pick_playerId`` : str — player's official ID

    Examples
    --------
    >>> import pypll
    >>> df = pypll.pll_draft_order(year=2025, league="PLL")
    >>> df[["round", "overallPick", "teamId", "pick_playerName", "pick_position"]].head()
       round  overallPick   teamId    pick_playerName pick_position
    0      1            1  ATLAS    John Smith             A
    1      1            2  CHROME   Mike Johnson           M
    """
    params = {"year": year, "league": league}
    response = _rest_get("/draft/order", params=params)
    items = response["data"]["items"]

    rows = []
    for item in items:
        row: dict = {}

        top_level_keys = ("id", "year", "round", "roundPick", "overallPick", "teamId", "league")
        for key in top_level_keys:
            row[key] = item.get(key)

        draft_pick = item.get("draftPick") or {}
        pick_keys = ("playerName", "college", "position", "playerId")
        for key in pick_keys:
            row[f"pick_{key}"] = draft_pick.get(key) if draft_pick else None

        rows.append(row)

    return pd.DataFrame(rows)


def pll_draft_predictions(year: int = 2026) -> pd.DataFrame:
    """Fetch PLL mock draft predictions from league analysts.

    Parameters
    ----------
    year : int, default 2026
        The draft year to retrieve predictions for. Predictions are typically
        published in the months leading up to the draft.

    Returns
    -------
    pd.DataFrame
        One row per analyst prediction with the following columns:

        - ``id`` : str — unique prediction record identifier
        - ``year`` : int — draft year
        - ``analystName`` : str — name of the analyst making the prediction
        - ``playerName`` : str — predicted player name
        - ``imageUrl`` : str — URL to the player image
        - ``position`` : str — player's position (e.g. "A", "M", "D", "G")
        - ``college`` : str — player's college
        - ``collegeLogo`` : str — URL to the college logo
        - ``overallRank`` : int — analyst's overall prospect ranking
        - ``positionRank`` : int — ranking within the player's position group
        - ``change`` : int — change in ranking from the previous update
        - ``analysis`` : str — analyst's written scouting notes
        - ``league`` : str — league identifier

    Examples
    --------
    >>> import pypll
    >>> df = pypll.pll_draft_predictions(year=2026)
    >>> df[["analystName", "playerName", "position", "overallRank", "college"]].head()
        analystName     playerName position  overallRank      college
    0  John Analyst  Connor Murphy        A            1  UNC
    1  John Analyst  Tyler Davis         M            2  Maryland
    """
    params = {"year": year}
    response = _rest_get("/draft/predictions", params=params)
    items = response["data"]["items"]
    return pd.DataFrame(items)


def pll_free_agents(year: int = 2026) -> pd.DataFrame:
    """Fetch PLL free agent signings and available players for a given year.

    This function queries the PLL GraphQL API. Data is available once free
    agency has opened for the specified year.

    Parameters
    ----------
    year : int, default 2026
        The free agency year to retrieve data for.

    Returns
    -------
    pd.DataFrame
        One row per free agent. Player identity fields are inlined at the top
        level alongside transaction fields:

        Player fields:

        - ``name`` : str — player's full name
        - ``firstName`` / ``lastName`` : str — player's first and last name
        - ``slug`` : str — URL slug
        - ``profileUrl`` : str — URL to the player profile page
        - ``age`` : int — player's age
        - ``experience`` : int — years of professional experience
        - ``position`` : str — position code (e.g. "A", "M", "D", "G")
        - ``status`` : str — player status

        Transaction fields:

        - ``officialId`` : str — unique player identifier
        - ``newContractStatus`` : str — contract status (e.g. "signed", "unsigned")
        - ``newTeamId`` : str — team the player signed with (None if unsigned)
        - ``prevTeamId`` : str — team the player was previously on
        - ``thirtyPercentThresholdMet`` : bool — whether the 30% salary threshold was met

    Examples
    --------
    >>> import pypll
    >>> df = pypll.pll_free_agents(year=2026)
    >>> df[["name", "position", "prevTeamId", "newTeamId", "newContractStatus"]].head()
                name position prevTeamId newTeamId newContractStatus
    0  Connor Martin        A      ATLAS    CHROME            signed
    1   Kyle Hartzell       D     CHROME      None         unsigned
    """
    response = _graphql_query(_FREE_AGENTS_QUERY, variables={"year": year})
    items = response["data"]["freeAgents"]

    rows = []
    for item in items:
        row: dict = {}

        # Inline nested player fields
        player = item.get("player") or {}
        for key, value in player.items():
            row[key] = value

        # Top-level fields
        top_level_keys = (
            "officialId",
            "newContractStatus",
            "newTeamId",
            "prevTeamId",
            "thirtyPercentThresholdMet",
        )
        for key in top_level_keys:
            row[key] = item.get(key)

        rows.append(row)

    return pd.DataFrame(rows)
