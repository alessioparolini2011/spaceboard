from textual.app import App, ComposeResult

from textual.widgets import Footer, Label, DataTable

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

        self.unit = True

    BINDINGS = [("e", "exit", "Close the program"), ("c", "change_units", "Units: (Metric/US)")]

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
    padding: 0 2
    }

    #neotab {
    width: auto;
    height: auto;
    color: #F0F8FF;
    background: #191970;
    }
    """

    def compose(self) -> ComposeResult:

        with Center():

            yield Label(r'''
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
          ''', id="title")

        with Center():    

            yield Label("This is [b]spaceboard[/b], a space weather dashboard to visualize NEO (Near Earth Objects) for today, yesterday and tomorrow.\nIt was created by Alessio Parolini in September 2026 for Hack Club X NASA event [b]Stardance[/b].",
                        id="des")

        table = DataTable(id="neotab")

        table.show_horizontal_scrollbar = True
        table.show_vertical_scrollbar = True
        table.cursor_type = "row"
        table.zebra_stripes = True

        yield table

        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:

        self.data_update(self.api)
    
    @work(thread=True)
    def data_update(self, api) -> None:

        self.list, self.list_US = neo_req(api)

        self.call_from_thread(self._store_data)



    def _store_data(self, day, imperial=False): #created in tab_update to not lose the 2 lists

            table = self.query_one("#neotab", DataTable)

            table.clear(columns=True)

            table.add_columns(
                "NAME", 
                "ID", 
                f"DIAMETER ({'ft' if imperial else 'm'})",
                f"SPEED ({'mph' if imperial else 'Km/h'})",
                f"DISTANCE ({'mi' if imperial else 'Km'})",
                "POTENTIALLY HAZARDOUS?"
            )
            
            for neo_object in (self.list if imperial else self.list_US):

                table.add_row(neo_object.name, neo_object.id, f"{neo_object.diam:,.3f}", f"{neo_object.speed:,.3f}", f"{neo_object.dis:,.3f}", "[red]YES!​⚠️​[/red]" if neo_object.hazard else "[green]NO[/green]")

    def action_exit(self) -> None:

        self.exit()

    def action_change_units(self) -> None:

        self._store_data(imperial=self.unit)

        self.unit = not self.unit