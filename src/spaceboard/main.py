"""
Welcome to my project, spaceboard! Is an software designed to visualize space data about NEOs (Near Earth Objects), like is a weather forecast, but for space!

My name is Alessio Parolini, and I am a software developer with a passion for creating innovative solutions.
"""

from spaceboard.tui_dashboard import Spaceboard

from spaceboard.onboard import OnBoard


def start():
    """
    Starts all the software
    """

    boarding = OnBoard()

    NASA_API_KEY = boarding.getapi()

    dates_id = boarding.getdates(limit=2)

    app = Spaceboard(
        api_key=NASA_API_KEY,
        dates_id=dates_id,
    )

    app.run()


if __name__ == "__main__":

    start()
