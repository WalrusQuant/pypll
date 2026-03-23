"""HTTP client internals for the PLL stats API."""

from __future__ import annotations

from typing import Any

import requests

_REST_BASE = "https://api.stats.premierlacrosseleague.com/api/v4"
_GRAPHQL_URL = "https://api.stats.premierlacrosseleague.com/graphql"

_REST_HEADERS = {
    "Authorization": "Bearer 2<b}_K/x8JU1mn/",
    "authSource": "stats",
    "Content-Type": "application/json",
}

_GRAPHQL_HEADERS = {
    "Authorization": "Bearer N)eIKy1rZ%/%fm1WhM7tuVcrR*UIsc",
    "Content-Type": "application/json",
}


def _rest_get(path: str, params: dict[str, Any] | None = None) -> Any:
    """Send a GET request to the PLL REST API.

    Args:
        path: URL path relative to the API base (e.g. "/standings").
        params: Optional query parameters.

    Returns:
        Parsed JSON response body.

    Raises:
        RuntimeError: On non-200 HTTP status or API-level error.
    """
    url = f"{_REST_BASE}{path}"
    response = requests.get(url, headers=_REST_HEADERS, params=params)

    if response.status_code != 200:
        raise RuntimeError(
            f"PLL REST API error {response.status_code} for {url}: {response.text}"
        )

    data = response.json()

    if isinstance(data, dict) and data.get("error"):
        raise RuntimeError(f"PLL REST API returned an error: {data['error']}")

    return data


def _graphql_query(query: str, variables: dict[str, Any] | None = None) -> Any:
    """Send a POST request to the PLL GraphQL API.

    Args:
        query: GraphQL query string.
        variables: Optional GraphQL variables.

    Returns:
        Parsed JSON response body.

    Raises:
        RuntimeError: On non-200 HTTP status or GraphQL errors in the response.
    """
    payload: dict[str, Any] = {"query": query}
    if variables is not None:
        payload["variables"] = variables

    response = requests.post(_GRAPHQL_URL, headers=_GRAPHQL_HEADERS, json=payload)

    if response.status_code != 200:
        raise RuntimeError(
            f"PLL GraphQL API error {response.status_code}: {response.text}"
        )

    data = response.json()

    if "errors" in data and data["errors"]:
        messages = "; ".join(e.get("message", str(e)) for e in data["errors"])
        raise RuntimeError(f"PLL GraphQL API returned errors: {messages}")

    return data
