'''
Welcome to my project, Spaceboard! Is an software designed to visualize space data, like is a weather forecast, but for space!

My name is Alessio Parolini, and I am a software developer with a passion for creating innovative solutions. 
'''

import httpx as hx

import os

from dotenv import load_dotenv

import json


def main(api):

    asteroid = hx.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2026-09-10&end_date=2026-09-15&api_key={api}") 

    if asteroid.status_code == 200:

        print("Request is good!")

        data = asteroid.json()

        with open("neo.json", "w") as file:

            json.dump(data, file)

    else:

        print("There is something wrong")

    return

    
if __name__ == "__main__":

    load_dotenv()

    NASA_API_KEY = os.getenv("NASA_API_KEY")

    main(NASA_API_KEY)