'''
Welcome to my project, Spaceboard! Is an software designed to visualize space data, like is a weather forecast, but for space!

My name is Alessio Parolini, and I am a software developer with a passion for creating innovative solutions. 
'''

import os

from dotenv import load_dotenv

from cli import spaceboard

def main():

    load_dotenv()
    
    NASA_API_KEY = os.getenv("NASA_API_KEY")

    app = spaceboard(api=NASA_API_KEY)

    app.run()
    
if __name__ == "__main__":

    main()