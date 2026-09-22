'''
Welcome to my project, Spaceboard! Is an software designed to visualize space data, like is a weather forecast, but for space!

My name is Alessio Parolini, and I am a software developer with a passion for creating innovative solutions. 
'''

import os

from dotenv import load_dotenv

import client

def main():

    load_dotenv()
    
    NASA_API_KEY = os.getenv("NASA_API_KEY")


    client.neo_req(NASA_API_KEY)
    
if __name__ == "__main__":

    main()