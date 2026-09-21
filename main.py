'''
Welcome to my project, Spaceboard! Is an software designed to visualize space data, like is a weather forecast, but for space!

My name is Alessio Parolini, and I am a software developer with a passion for creating innovative solutions. 
'''

import httpx as hx

NASA_API_KEY = "" #put yours

def main(api):

    asteroid = hx.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2026-09-10&end_date=2026-09-15&api_key={api}") 

    if asteroid.status_code == 200:

        print("Request is good!")

        print(asteroid.json())

    else:

        print("There is something wrong")

    return

    

main(NASA_API_KEY)