import httpx as hx

import json as js

import datetime as dt


class asteroid: #creating the class to saves NEOs with 

    def __init__(self, name: str, id: str, diameter: float, speed: float, dis: float, orbit: str, hazard: bool):

        self.name = name

        self.id = id

        self.diam = diameter

        self.speed = speed

        self.dis = dis

        self.orbit = orbit 

        self.hazard = hazard

class asteroidUs: #creating the class to save NEOs with US metric

    def __init__(self, name: str, id: str, diameter: float, speed: float, dis: float, orbit: str, hazard: bool):

        self.name = name

        self.id = id

        self.diam = diameter

        self.speed = speed

        self.dis = dis

        self.orbit = orbit

        self.hazard = hazard

def neo_req(api):

    current_date = dt.date.today() #get the current data for the reqeust

    today = current_date.isoformat()

    yesterday = current_date - dt.timedelta(days=1)

    tomorrow = current_date + dt.timedelta(days=1)

    asteroid = hx.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date={yesterday}&end_date={tomorrow}&api_key={api}")

    if asteroid.status_code == 200:

        print("\n--RESOURCES ACHIVED SUCCESSFULLY--\nREQUEST ENDED\n")

        data = asteroid.json()

        return classifier(json=data, today=today, yesterday=yesterday, tomorrow=tomorrow)


    else:

        print(f"\n--ERROR: {asteroid.status_code}--\nSOMETHING WENT WRONG\n")

    return

def classifier(json, today, tomorrow, yesterday) -> tuple[list[asteroid], list[asteroid], list[asteroid]]:

    td_asteroids: list[asteroid] = []

    yd_asteroids: list[asteroid] = []

    tm_asteroids: list[asteroid] = []



    for day in json["near_earth_object"]:

        if day == today:

            for neo in json[today]:

                diameter = (neo["estimated_diameter"]["meters"]["estimated_diameter_min"]+neo["estimated_diameter"]["meters"]["estimated_diameter_max"])/2

                approach = neo["close_approach_data"][0] #get the closest approach datas (only takes the first approach, most of times is the only. )

                if approach["orbiting_body"] == "Earth":

                    neo = asteroid(name=neo["name"], 
                             id=neo["id"], 
                             diameter=diameter.round(2), 
                             speed=approach["relative_velocity"]["kilometers_per_hour"].round(2), 
                             dis=approach["miss_distance"]["kilometres."].round(2),
                             orbit = approach["orbiting_body"],
                             hazard= neo["is_potentially_hazardous_asteroid"])

                    td_asteroids.append(neo)

        if day == yesterday:

            for neo in json[yesterday]:

                diameter = (neo["estimated_diameter"]["meters"]["estimated_diameter_min"]+neo["estimated_diameter"]["meters"]["estimated_diameter_max"])/2

                approach = neo["close_approach_data"][0] #get the closest approach datas (only takes the first approach, most of times is the only. )

                if approach["orbiting_body"] == "Earth":

                    neo = asteroid(name=neo["name"], 
                             id=neo["id"], 
                             diameter=diameter.round(2), 
                             speed=approach["relative_velocity"]["kilometers_per_hour"].round(2), 
                             dis=approach["miss_distance"]["kilometres."].round(2),
                             orbit = approach["orbiting_body"],
                             hazard= neo["is_potentially_hazardous_asteroid"])

                    yd_asteroids.append(neo)

        if day == tomorrow:

            for neo in json[tomorrow]:

                diameter = (neo["estimated_diameter"]["meters"]["estimated_diameter_min"]+neo["estimated_diameter"]["meters"]["estimated_diameter_max"])/2

                approach = neo["close_approach_data"][0] #get the closest approach datas (only takes the first approach, most of times is the only. )

                if approach["orbiting_body"] == "Earth":

                    neo = asteroid(name=neo["name"], 
                             id=neo["id"], 
                             diameter=diameter.round(2), 
                             speed=approach["relative_velocity"]["kilometers_per_hour"].round(2), 
                             dis=approach["miss_distance"]["kilometres."].round(2),
                             orbit = approach["orbiting_body"],
                             hazard= neo["is_potentially_hazardous_asteroid"])

                    tm_asteroids.append(neo) 

    print("\n--RESOURCES STORED SUCCESSFULLY--\n")

    return td_asteroids, yd_asteroids, tm_asteroids #return the lists of neos