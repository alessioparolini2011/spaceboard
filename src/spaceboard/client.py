"""
NASA NEO API client for Spaceboard

This module provides utilities to fetch and process Near Earth Object (NEO) data from NASA API, converting it it into structured Python objects.
"""

import httpx as hx
from dataclasses import dataclass

# HTTP client configuration

_client = hx.Client(timeout=30.0, base_url="https://api.nasa.gov")


class NasaError(Exception):
    """Custom exception for NASA API errors"""

    pass


@dataclass
class Neo:
    """
    Represents a NEO with his data

    Attributes:
        name: object name
        id: NASA internal ID
        data: Date to closest approach (ISO format)
        diameter: average diameter in specified units
        speed: relative velocity in specified units
        distance: miss distance in specified units
        hazard: whether it's potentially hazardous
    """

    name: str

    id: str

    link: str

    date: str

    diameter: float

    speed: float

    distance: float

    hazard: bool


def fetch_neo_data(
    api_key: str, start_date: str, end_date: str
) -> tuple[list[Neo], list[Neo]]:
    """
    Fetch NEO data from NASA API and return both metric and imperial units

    Args:
        api_key: NASA API key
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        tuple of (metric_neos, imperial_neos)

    Raises:
        NasaError: If API request fails
    """

    try:

        response = _client.get(
            "neo/rest/v1/feed",
            params={"start_date": start_date, "end_date": end_date, "api_key": api_key},
        )

        response.raise_for_status()

    except hx.HTTPStatusError as e:

        code = e.response.status_code

        if code in (401, 403):

            raise NasaError(
                f"NASA Server error: {code}. There's an error with your API key."
            ) from e

        elif code == 429:

            raise NasaError(
                f"NASA Server error: {code}. You hit the rate limit. If you're using a DEMO_KEY (with only 50 requets for day), change to a personal one.\nIf instead you're using a personal one, you've to wait for an hour."
            ) from e

        elif 500 <= code <= 600:

            raise NasaError(
                f"NASA Server error: {code}. NASA server is down, try later."
            ) from e

    except hx.TimeoutException as e:

        raise NasaError(
            f"Timeout expired. Check your connection, maybe is too slow. Error: {e}"
        )

    except hx.ConnectError as e:

        raise NasaError(f"You've got no Internet connection! Error: {e}")

    except hx.RequestError as e:

        raise NasaError(f"Generic network error: {e}")

    neo_data = response.json()

    return _parse_neo_response(data=neo_data)


def _parse_neo_response(data: dict) -> tuple[list[Neo], list[Neo]]:
    """
    Parse NASA API response and convert to Neo objects in both metric and imperial units

    Args:

        data: the JSON from the NASA API

    Returns:

        a tuple with two lists, one for NEO in metric and one for NEO in imperial
    """

    metric_neos: Neo = []

    imperial_neos: Neo = []

    for date_str, objects in data["near_earth_objects"].items():

        for obj in objects:

            # does some operations for get special datas (average extimated diameter and the data of the closest approach)

            diameter_metric = (
                obj["estimated_diameter"]["meters"]["estimated_diameter_min"]
                + obj["estimated_diameter"]["meters"]["estimated_diameter_max"]
            ) / 2

            diameter_imperial = (
                obj["estimated_diameter"]["feet"]["estimated_diameter_min"]
                + obj["estimated_diameter"]["feet"]["estimated_diameter_max"]
            ) / 2

            approach = obj["close_approach_data"][0]  # get the closest approach datas

            if (
                approach["orbiting_body"] != "Earth"
            ):  # get the data only if the NEO pass near Earth

                continue

            common_attrs = {
                "name": obj["name"],
                "id": obj["id"],
                "link": obj["nasa_jpl_url"],
                "date": date_str,
                "hazard": obj["is_potentially_hazardous_asteroid"],
            }

            neo_metric = Neo(
                **common_attrs,
                diameter=diameter_metric,
                speed=float(approach["relative_velocity"]["kilometers_per_hour"]),
                distance=float(approach["miss_distance"]["kilometers"]),
            )
            metric_neos.append(neo_metric)

            neo_imperial = Neo(
                **common_attrs,
                diameter=diameter_imperial,
                speed=float(approach["relative_velocity"]["miles_per_hour"]),
                distance=float(approach["miss_distance"]["miles"]),
            )

            imperial_neos.append(neo_imperial)

    return metric_neos, imperial_neos
