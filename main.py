'''
Welcome to my project, Spaceboard! Is an software designed to visualize space data, like is a weather forecast, but for space!

My name is Alessio Parolini, and I am a software developer with a passion for creating innovative solutions. 
'''

import os

from dotenv import load_dotenv

from cli import spaceboard

from client import neo_req

def main():

    load_dotenv()
    
    NASA_API_KEY = os.getenv("NASA_API_KEY")


    neo_req(NASA_API_KEY)

    app = spaceboard()

    app.run()
    
if __name__ == "__main__":

    main()