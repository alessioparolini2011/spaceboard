"""
Welcome to my project, Spaceboard! Is an software designed to visualize space data, like is a weather forecast, but for space!

My name is Alessio Parolini, and I am a software developer with a passion for creating innovative solutions.
"""

from cli import spaceboard

import datetime as dt

from onboard import OnBoard


def main():

    boarding = OnBoard()

    NASA_API_KEY = boarding.getapi()

    dates_id = boarding.getdates(limit=1)

    app = spaceboard(
        api=NASA_API_KEY,
        dates_id=dates_id,
    )

    app.run()


if __name__ == "__main__":

    main()
