from textual.app import App, ComposeResult

from textual.widgets import Footer, Label, DataTable

from textual.containers import Center

from textual import work

from client import neo_req, neo, neoUs


class spaceboard(App):

    def __init__(self, api, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.api = api

    BINDINGS = [("e", "exit", "Close the program"), ("r", "refresh_data", "Refresh datas")]

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
    min-width: 100%;
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

        yield Footer()

    def on_mount(self) -> None:

        table = self.query_one("#neotab", DataTable)

        table.add_columns("NAME", "ID", "DIAMETER (m)", "SPEED (Km/h)", "DISTANCE (Km)", "POTENTIALLY HAZARDOUS?" )

        self.tab_update(self.api)

    
    @work(thread=True)
    def tab_update(self, api) -> None:

        table = self.query_one("#neotab", DataTable)

        neo_list, neo_list_US = neo_req(api)

        for neo_object in neo_list:

            table.add_row(neo_object.name, neo_object.id, neo_object.diam, neo_object.speed, neo_object.dis, "[red]YES!​⚠️​[/red]" if neo_object.hazard else "[green]NO[/green]")

    def action_exit(self) -> None:

        self.exit()


    def action_refresh_data(self) -> None:

        table = self.query_one("#neotab", DataTable)

        table.clear()

        self.tab_update(self.api)