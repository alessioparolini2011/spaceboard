import httpx as hx

import json as js

class asteroid: #creating the class to saves NEOs

    def __init__(self, name, id, diameter_m, diameter_f, hazard ):

        self.name = name

        self.id = id

        self.diam_m = diameter_m

        self.diam_f = diameter_f

        self.hazard = hazard

def neo_req(api):

    asteroid = hx.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2026-09-10&end_date=2026-09-15&api_key={api}")

    if asteroid.status_code == 200:

        print("--RESOURCES ACHIVED SUCCESSFULLY--\nREQUEST ENDED")

    else:

        print(f"--ERROR: {asteroid.status_code}--\nSOMETHING WENT WRONG")

    return

