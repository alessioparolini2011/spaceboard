from textual.app import App, ComposeResult

from textual.widgets import Footer, Label, DataTable, ContentSwitcher

from textual.containers import Center

from textual import work

from client import neo_req, neo, neoUs


class spaceboard(App):

    def __init__(self, api, today, yesterday, tomorrow, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.api = api

        self.td = today

        self.yd = yesterday

        self.tm = tomorrow

        self.list: neo = []

        self.list_US: neoUs = []

        self.state = True

        self.days = ["td", "tm", "yd"]

    BINDINGS = [
        ("e", "exit", "Close the program"),
        ("c", "change_units", "Units: (Metric/US)"),
    ]

    CSS = """
    #title {
    color: #00FFFF;
    text-align: center;
    height: auto; 
    width: auto;}

    #des {
    color: #F0F8FF;
    text-align: center;
    height: auto;
    width:auto;
    margin: 1;
    border: round #F0F8FF;
    padding: 0 2;
    }

    ContentSwitcher {
    
    width: 100%;
    height: auto;
    margin: 2 2;

    }

    .neotab {
    width: 100%;
    height: auto;
    color: #F0F8FF;
    background: #191970;
    }
    """

    def compose(self) -> ComposeResult:

        with Center():

            yield Label(
                r"""
                                                   /$$                                           /$$
                                                  | $$                                          | $$
  /$$$$$$$  /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$
 /$$_____/ /$$__  $$ |____  $$ /$$_____/ /$$__  $$| $$__  $$ /$$__  $$ |____  $$ /$$__  $$ /$$__  $$
|  $$$$$$ | $$  \ $$  /$$$$$$$| $$      | $$$$$$$$| $$  \ $$| $$  \ $$  /$$$$$$$| $$  \__/| $$  | $$
 \____  $$| $$  | $$ /$$__  $$| $$      | $$_____/| $$  | $$| $$  | $$ /$$__  $$| $$      | $$  | $$
 /$$$$$$$/| $$$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$$$$$$/|  $$$$$$/|  $$$$$$$| $$      |  $$$$$$$
|_______/ | $$____/  \_______/ \_______/ \_______/|_______/  \______/  \_______/|__/       \_______/
          | $$                                                                                      
          | $$                                                                                      
          |__/                                                                                      
          """,
                id="title",
            )

        with Center():

            yield Label(
                "This is [b]spaceboard[/b], a space weather dashboard to visualize NEO (Near Earth Objects) for current, previous and next day.\nIt was created by Alessio Parolini in September 2026 for Hack Club X NASA event [b]Stardance[/b].",
                id="des",
            )

        td_table = DataTable(
            classes="neotab",
            id="tdt",
            cursor_type="row",
            zebra_stripes=True,
            cell_padding=3,
        )

        td_table_US = DataTable(
            classes="neotab",
            id="tdt_US",
            cursor_type="row",
            zebra_stripes=True,
            cell_padding=3,
        )

        yd_table = DataTable(
            classes="neotab",
            id="ydt",
            cursor_type="row",
            zebra_stripes=True,
            cell_padding=3,
        )

        yd_table_US = DataTable(
            classes="neotab",
            id="ydt_US",
            cursor_type="row",
            zebra_stripes=True,
            cell_padding=3,
        )

        tm_table = DataTable(
            classes="neotab",
            id="tmt",
            cursor_type="row",
            zebra_stripes=True,
            cell_padding=3,
        )

        tm_table_US = DataTable(
            classes="neotab",
            id="tmt_US",
            cursor_type="row",
            zebra_stripes=True,
            cell_padding=3,
        )

        with ContentSwitcher(initial="tdt"):

            yield td_table

            yield td_table_US

            yield yd_table

            yield yd_table_US

            yield tm_table

            yield tm_table_US

        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:

        self.data_update(self.api)

    @work(thread=True)
    def data_update(self, api) -> None:

        self.neo_list, self.neo_list_US = neo_req(
            api, today=self.td, yesterday=self.yd, tomorrow=self.tm
        )

        self.call_from_thread(self._store_data)

    def _store_data(self):

        tdt = self.query_one("#tdt", DataTable)

        tdt_US = self.query_one("#tdt_US", DataTable)

        ydt = self.query_one("#ydt", DataTable)

        ydt_US = self.query_one("#ydt_US", DataTable)

        tmt = self.query_one("#tmt", DataTable)

        tmt_US = self.query_one("#tmt_US", DataTable)

        day_tables = [
            (
                self.td,
                tdt,
                tdt_US,
            ),
            (
                self.yd,
                ydt,
                ydt_US,
            ),
            (
                self.tm,
                tmt,
                tmt_US,
            ),
        ]

        for target_date, table_metric, table_US in day_tables:

            table_metric.add_columns(
                "[b]NAME[b/]",
                "[b]ID[b/]",
                "[b]DIAMETER (m)[b/]",
                "[b]SPEED (Km/h)[b/]",
                "[b]DISTANCE (Km)[b/]",
                "[b]POTENTIALLY HAZARDOUS?[b/]",
            )

            table_US.add_columns(
                "[b]NAME[b/]",
                "[b]ID[b/]",
                "[b]DIAMETER (ft)[b/]",
                "[b]SPEED (mph)[b/]",
                "[b]DISTANCE (mi)[b/]",
                "[b]POTENTIALLY HAZARDOUS?[b/]",
            )

            for neo_object in self.neo_list:

                if neo_object.date == target_date:

                    table_metric.add_row(
                        f"\n{neo_object.name}",
                        f"\n{neo_object.id}",
                        f"\n{neo_object.diam:,.3f}",
                        f"\n{neo_object.speed:,.3f}",
                        f"\n{neo_object.dis:,.3f}",
                        (
                            "\n[red]YES!​⚠️​[/red]"
                            if neo_object.hazard
                            else "\n[green]NO[/green]"
                        ),
                        height=3,
                    )

            for neo_object_US in self.neo_list_US:

                if neo_object_US.date == target_date:

                    table_US.add_row(
                        f"\n{neo_object_US.name}",
                        f"\n{neo_object_US.id}",
                        f"\n{neo_object_US.diam:,.3f}",
                        f"\n{neo_object_US.speed:,.3f}",
                        f"\n{neo_object_US.dis:,.3f}",
                        (
                            "\n[red]YES!​⚠️​[/red]"
                            if neo_object_US.hazard
                            else "\n[green]NO[/green]"
                        ),
                        height=3,
                    )

        self.notify("Data stored successfully!")

    def action_exit(self) -> None:

        self.exit()

    def action_change_units(self) -> None:

        switcher = self.query_one(ContentSwitcher)

        current = switcher.current

        if current.endswith("_US"):

            new_t = current.replace("_US", "")

        else:

            new_t = f"{current}_US"

        switcher.current = new_t
