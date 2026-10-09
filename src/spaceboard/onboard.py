import os

from dotenv import load_dotenv, set_key

from pathlib import Path

import datetime as dt

from rich.console import Console

ENV_PATH = Path.home() / ".spaceboard_env"


class OnBoard:

    def __init__(self):

        self.console = Console()

        pass

    def getapi(self) -> str:

        if not ENV_PATH.exists():

            ENV_PATH.touch()

        load_dotenv(dotenv_path=ENV_PATH)

        NASA_API_KEY: str = os.getenv("NASA_API_KEY")

        if NASA_API_KEY and NASA_API_KEY.strip():

            return NASA_API_KEY

        else:

            self.console.print(
                """[red]There isn't any NASA API key[/]. [bold]You need to get one[/].\n\n
            [bold]IMPORTANT[/]: if you want to do a fast try, enter "DEMO_KEY". You'll get less requests but it's perfect to a fast look!\n\n
            Else, you can get a [bold]personal API KEY following[/] this steps:\n
            1. Go to https://api.nasa.gov/.\n
            2. Create your own by entering some data (name and e-mail).\n
            3. Check your inbox (for the e-mail account you used) and look for a NASA message\n
            4. Copy the API key and paste it here:"""
            )

            user_input = ""

            while not user_input.strip():

                user_input = self.console.input("\n[blue]->[/] ")

            NASA_API_KEY = user_input.strip()

            set_key(ENV_PATH, "NASA_API_KEY", NASA_API_KEY)

            return NASA_API_KEY

    def getdates(self, limit) -> dict:

        cd = dt.date.today()

        dates_id = {"cd": [(cd,), ()]}

        for i in range(1, limit + 1):

            pd_id = cd - dt.timedelta(days=i)

            nd_id = cd + dt.timedelta(days=i)

            dates_id.update({f"pd{i}": [(pd_id,), ()], f"nd{i}": [(nd_id,), ()]})

        return dates_id
