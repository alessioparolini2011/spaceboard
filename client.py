import httpx as hx

import json as js

import datetime as dt


class asteroid: #creating the class to saves NEOs with 

    def __init__(self, name: str, id: str, date: str, diameter: float, speed: float, dis: float, orbit: str, hazard: bool):

        self.name = name

        self.id = id

        self.date = date

        self.diam = diameter

        self.speed = speed

        self.dis = dis

        self.orbit = orbit 

        self.hazard = hazard

class asteroidUs: #creating the class to save NEOs with US metric

    def __init__(self, name: str, id: str, date: str, diameter: float, speed: float, dis: float, orbit: str, hazard: bool):

        self.name = name

        self.id = id

        self.date = date

        self.diam = diameter

        self.speed = speed

        self.dis = dis

        self.orbit = orbit

        self.hazard = hazard

def neo_req(api):

    current_date = dt.date.today() #get the current data for the reqeust

    today = current_date.isoformat()

    yesterday = (current_date - dt.timedelta(days=1)).isoformat()

    tomorrow = (current_date + dt.timedelta(days=1)).isoformat()

    asteroid = hx.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date={yesterday}&end_date={tomorrow}&api_key={api}")

    if asteroid.status_code == 200:

        print("\n--RESOURCES ACHIVED SUCCESSFULLY--\nREQUEST ENDED\n")

        data = asteroid.json()

        return classifier(json=data, today=today, yesterday=yesterday, tomorrow=tomorrow)


    else:

        print(f"\n--ERROR: {asteroid.status_code}--\nSOMETHING WENT WRONG\n")

    return

def classifier(json, today, tomorrow, yesterday) -> tuple[list[asteroid], list[asteroid]]:

    asteroids: asteroid = [] #to save neos with standard metric

    asteroidsUS : asteroid = [] #to save neos with US metric

    for day, neos_list in json["near_earth_objects"].items():

        for neos in neos_list:

            diameter = (neos["estimated_diameter"]["meters"]["estimated_diameter_min"]+neos["estimated_diameter"]["meters"]["estimated_diameter_max"])/2

            diameterUS = (neos["estimated_diameter"]["feet"]["estimated_diameter_min"]+neos["estimated_diameter"]["feet"]["estimated_diameter_max"])/2

            approach = neos["close_approach_data"][0] #get the closest approach datas (only takes the first approach, most of times is the only. )

            if approach["orbiting_body"] == "Earth":

                neo = asteroid(name=neos["name"], 
                                id=neos["id"], 
                                date=day,
                                diameter=diameter, 
                                speed=float(approach["relative_velocity"]["kilometers_per_hour"]), 
                                dis=float(approach["miss_distance"]["kilometers"]),
                                orbit = approach["orbiting_body"],
                                hazard= neos["is_potentially_hazardous_asteroid"])

                neoUS = asteroid(name=neos["name"], 
                                id=neos["id"], 
                                date=day,
                                diameter=diameterUS, 
                                speed=float(approach["relative_velocity"]["miles_per_hour"]), 
                                dis=float(approach["miss_distance"]["miles"]),
                                orbit = approach["orbiting_body"],
                                hazard= neos["is_potentially_hazardous_asteroid"])

                asteroids.append(neo)

                asteroidsUS.append(neoUS)

    print("\n--RESOURCES STORED SUCCESSFULLY--\n")

    return asteroids #return the lists of neos