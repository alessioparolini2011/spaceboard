import os

from dotenv import load_dotenv, set_key

import datetime as dt

from rich.console import Console


class OnBoard:

    def __init__(self):

        self.console = Console()

        pass

    def getapi(self) -> str:

        load_dotenv()

        NASA_API_KEY = os.getenv("NASA_API_KEY")

        if NASA_API_KEY:

            return NASA_API_KEY

        else:

            self.console.print(
                """[red]There isn't any NASA API key[/]. [bold]You need to create one[/].\n\n
            1. Go to https://api.nasa.gov/.\n
            2. Create your own by entering some data (name and e-mail).\n
            3. Check your inbox (for the e-mail account you used) and look for a NASA message\n
            4. Copy the API key and paste it here:"""
            )

            while not NASA_API_KEY:

                NASA_API_KEY = self.console.input("[blue]->[/] ")

            set_key(".env", "NASA_API_KEY", NASA_API_KEY)

            return NASA_API_KEY

    def getdates(self, limit) -> dict:

        cd = dt.date.today()

        dates_id = {"cd": [(cd,), ()]}

        for i in range(1, limit + 1):

            pd_id = cd - dt.timedelta(days=i)

            nd_id = cd + dt.timedelta(days=i)

            dates_id.update({f"pd{i}": [(pd_id,), ()], f"nd{i}": [(nd_id,), ()]})

        return dates_id
