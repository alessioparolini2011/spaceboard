import httpx as hx

import json as js

import datetime as dt


class asteroid: #creating the class to saves NEOs with 

    def __init__(self, name, id, diameter, speed, dis, orbit, hazard):

        self.name = name

        self.id = id

        self.diam = diameter

        self.speed = speed

        self.dis = dis

        self.orbit = orbit 

        self.hazard = hazard

class asteroidUs: #creating the class to save NEOs with US metric

    def __init__(self, name, id, diameter, speed, dis, orbit, hazard):

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

        print("--RESOURCES ACHIVED SUCCESSFULLY--\nREQUEST ENDED")

        data = asteroid.json()

    else:

        print(f"--ERROR: {asteroid.status_code}--\nSOMETHING WENT WRONG")

    return

def classifier(json, today, tomorrow, yesterday):

    for day in json["near_earth_object"]:

        if day == today:

            for neo in json[today]:

                diameter = (neo["estimated_diameter"]["meters"]["estimated_diameter_min"]+neo["estimated_diameter"]["meters"]["estimated_diameter_maz"])/2

                approach = neo["close_approach_data"][0] #get the closest approach datas (only takes the first approach, most of times is the only. )

                if approach["orbiting_body"] == "Earth":

                    asteroid(name=neo["name"], id=neo["id"], diameter=diameter, speed=approach["relative_velocity"]["kilometers_per_hour"], dis=approach )