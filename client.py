import httpx as hx

import json as js

client = hx.Client(timeout=30.0, base_url="https://api.nasa.gov")


class NasaError(Exception):

    pass


class neo:  # creating the class to saves NEOs with

    def __init__(
        self,
        name: str,
        id: str,
        date: str,
        diameter: float,
        speed: float,
        dis: float,
        hazard: bool,
    ):

        self.name = name

        self.id = id

        self.date = date

        self.diam = diameter

        self.speed = speed

        self.dis = dis

        self.hazard = hazard


class neoUs:  # creating the class to save NEOs with US metric

    def __init__(
        self,
        name: str,
        id: str,
        date: str,
        diameter: float,
        speed: float,
        dis: float,
        hazard: bool,
    ):

        self.name = name

        self.id = id

        self.date = date

        self.diam = diameter

        self.speed = speed

        self.dis = dis

        self.hazard = hazard


def neo_req(api, start_day, end_day):

    try:

        request = client.get(
            "neo/rest/v1/feed",
            params={"start_date": start_day, "end_date": end_day, "api_key": api},
        )

        request.raise_for_status()

    except hx.HTTPStatusError as e:
        code = e.response.status_code
        if code in (401, 403):
            raise NasaError(
                f"Nasa Server Error: {code}. Check your API key in the .env file. Is it correct? If you're not sure, [bold]delete it and restart the file - you'll be help to get a right one![/]"
            ) from e
        elif code == 429:
            raise NasaError(
                f"Nasa Server Error: {code}. Rate limit exceeded. Use a personal API key."
            ) from e
        elif 500 <= code < 600:
            raise NasaError(
                f"Nasa Server Error: {code}. NASA server is down, try later."
            ) from e
        else:
            raise NasaError(f"Nasa Server Error: {code}") from e

    except hx.TimeoutException as e:

        raise NasaError("Timeout expired.") from e

    except hx.ConnectError as e:

        raise NasaError(f"No connection with NASA Server: {e}") from e

    except hx.RequestError as e:

        raise NasaError(f"Generic network error: {e}") from e

    data = request.json()

    return classifier(json_data=data)


def classifier(json_data) -> tuple[list[neo], list[neoUs]]:

    neo_list: neo = []  # to save neos with standard metric

    neo_list_US: neoUs = []  # to save neos with US metric

    for day, neos_list in json_data["near_earth_objects"].items():

        for neos in neos_list:

            diameter = (
                neos["estimated_diameter"]["meters"]["estimated_diameter_min"]
                + neos["estimated_diameter"]["meters"]["estimated_diameter_max"]
            ) / 2

            diameterUS = (
                neos["estimated_diameter"]["feet"]["estimated_diameter_min"]
                + neos["estimated_diameter"]["feet"]["estimated_diameter_max"]
            ) / 2

            approach = neos["close_approach_data"][
                0
            ]  # get the closest approach datas (only takes the first approach, most of times is the only. )

            if approach["orbiting_body"] == "Earth":

                neo_object = neo(
                    name=neos["name"],
                    id=neos["id"],
                    date=day,
                    diameter=diameter,
                    speed=float(approach["relative_velocity"]["kilometers_per_hour"]),
                    dis=float(approach["miss_distance"]["kilometers"]),
                    hazard=neos["is_potentially_hazardous_asteroid"],
                )

                neoUS_object = neoUs(
                    name=neos["name"],
                    id=neos["id"],
                    date=day,
                    diameter=diameterUS,
                    speed=float(approach["relative_velocity"]["miles_per_hour"]),
                    dis=float(approach["miss_distance"]["miles"]),
                    hazard=neos["is_potentially_hazardous_asteroid"],
                )

                neo_list.append(neo_object)

                neo_list_US.append(neoUS_object)

    print("\n--RESOURCES STORED SUCCESSFULLY--\n")

    return neo_list, neo_list_US  # return the lists of neos
