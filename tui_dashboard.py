"""
cli.py
This file uses Textual for create and manage an interactive CLI.
"""

from rich.align import Align

from rich.text import Text

from textual.app import App, ComposeResult

from textual.widgets import Footer, Label, DataTable, ContentSwitcher

from textual.screen import ModalScreen

from textual.containers import Center, Vertical

from textual.binding import Binding

from textual import work

from client import fetch_neo_data, NasaError


class ErrorScreen(
    ModalScreen
):  # creating a class (from ModalScreen) to visualize errors

    BINDINGS = [("e", "escape", "Close the window")]

    CSS_PATH = "tcss/error_screen.tcss"

    def __init__(
        self, name=None, id=None, classes=None, *, message: str = "Unknown Error!"
    ):
        super().__init__(name, id, classes)

        self.message = message

    def compose(self):

        with Center():

            with Vertical():

                yield Label(
                    """[red]                                   
    ###### #####  #####   ####  #####  
    #      #    # #    # #    # #    # 
    #####  #    # #    # #    # #    # 
    #      #####  #####  #    # #####  
    #      #   #  #   #  #    # #   #  
    ###### #    # #    #  ####  #    # [/red]""",
                    id="bigError",
                )

                yield Label(self.message, id="errorMessage", markup=True)

                yield Label("(Press 'e' to exit)", id="exitMessage")

    def action_escape(self):

        self.dismiss()


class MiddleTxt(Align):
    def __init__(self, text: str, height: int = 3):
        super().__init__(
            Text.from_markup(text, justify="center"),
            vertical="middle",
            height=height,
        )


class Spaceboard(App):

    BINDINGS = [
        Binding(
            "left",
            "go_left",
            "Go left (use left arrow key)",
            show=True,
            priority=True,
        ),
        Binding(
            "right",
            "go_right",
            "Go right (use right arrow key)",
            show=True,
            priority=True,
        ),
        Binding(
            "c",
            "toggle_units",
            "Units: (Metric/Imperial)",
            show=True,
            priority=True,
        ),
        Binding(
            "q",
            "quit",
            "Close the program",
            show=True,
            priority=True,
        ),
    ]

    CSS_PATH = "tcss/spaceboard.tcss"

    COLUMNS_METRIC = [
        "[b]NAME[/b]",
        "[b]ID[/b]",
        "[b]DIAMETER (m)[/b]",
        "[b]SPEED (Km/h)[/b]",
        "[b]DISTANCE (Km)[/b]",
        "[b]POTENTIALLY HAZARDOUS?[/b]",
    ]

    COLUMNS_IMPERIAL = [
        "[b]NAME[/b]",
        "[b]ID[/b]",
        "[b]DIAMETER (ft)[/b]",
        "[b]SPEED (mph)[/b]",
        "[b]DISTANCE (mi)[/b]",
        "[b]POTENTIALLY HAZARDOUS?[/b]",
    ]

    def __init__(self, api: str, dates_id: dict, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.api = api

        self.dates_id = dates_id

        self.ordered_days_list = sorted(
            self.dates_id.keys(), key=lambda k: self.dates_id[k][0][0]
        )

        self.day_index = self.ordered_days_list.index("cd")

        self.neo_by_unit = {"metric": [], "imperial": []}

        self.is_metric = True

    def make_table_group(self, tid: str) -> Vertical:

        label = Label("", id=f"{tid}_label", classes="tableDateLabel")

        table = DataTable(
            classes="neoTab",
            id=f"{tid}_table",
            cursor_type="row",
            zebra_stripes=True,
            cell_padding=3,
        )

        return Vertical(
            label,
            table,
            id=tid,
        )

    def _add_new_row(self, table: DataTable, neo_obj):
        table.add_row(
            MiddleTxt(f"[link={neo_obj.link}]{neo_obj.name}[/link]"),
            MiddleTxt(neo_obj.id),
            MiddleTxt(f"{neo_obj.diameter:,.3f}"),
            MiddleTxt(f"{neo_obj.speed:,.3f}"),
            MiddleTxt(f"{neo_obj.distance:,.3f}"),
            MiddleTxt(
                ("[bold red]YES! ⚠️[/]" if neo_obj.hazard else "[bold green]NO[/]")
            ),
            height=3,
        )

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

            description = Label(
                "This is [b]spaceboard[/b], a very simple space weather dashboard to visualize NEOs (Near Earth Objects) data for a 5-days window (current day and the 2 next/previous).\nIt was created by Alessio Parolini in September 2026 for Hack Club X NASA event [b]Stardance[/b].",
                id="des",
            )

            description.border_title = "What's this?"

            yield description

        with ContentSwitcher(
            initial=list(self.dates_id.keys())[0], id="table_switcher"
        ):

            for day_id in self.dates_id.keys():

                yield self.make_table_group(day_id)

                yield self.make_table_group(f"{day_id}_imperial")

        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:

        self.switcher = self.query_one("#table_switcher", ContentSwitcher)

        self.data_update(self.api)

    @work(thread=True)
    def data_update(self, api) -> None:

        limit_days = (list(self.dates_id.keys())[-2], list(self.dates_id.keys())[-1])

        try:

            metric, imperial = fetch_neo_data(
                api_key=api,
                start_date=self.dates_id[limit_days[0]][0][0],
                end_date=self.dates_id[limit_days[1]][0][0],
            )

        except NasaError as e:

            self.call_from_thread(self.push_screen, ErrorScreen(message=str(e)))

            return

        if metric and imperial:

            self.call_from_thread(self.notify, "Datas achived successfully!")

            self.neo_by_unit["metric"] = metric

            self.neo_by_unit["imperial"] = imperial

            self.call_from_thread(self._store_data)

    def _store_data(self):

        max_rows = 0

        for key in self.dates_id:
            self.dates_id[key][1] = (
                self.query_one(f"#{key}_table", DataTable),
                self.query_one(f"#{key}_imperial_table", DataTable),
                self.query_one(f"#{key}_label"),
                self.query_one(f"#{key}_imperial_label"),
            )

        for (target_date,), (
            table_metric,
            table_imperial,
            label_metric,
            label_imperial,
        ) in self.dates_id.values():

            label_metric.styles.border = "round", "#F0F8FF"

            label_metric.update(target_date.strftime("%A %d %B %Y"))

            label_imperial.styles.border = "round", "#F0F8FF"

            label_imperial.update(target_date.strftime("%A %d %B %Y"))

            table_metric.add_columns(*self.COLUMNS_METRIC)

            table_imperial.add_columns(*self.COLUMNS_IMPERIAL)

            neos_metric = [
                n
                for n in self.neo_by_unit["metric"]
                if n.date == target_date.isoformat()
            ]

            neos_imperial = [
                n
                for n in self.neo_by_unit["imperial"]
                if n.date == target_date.isoformat()
            ]

            for neo_m in neos_metric:

                self._add_new_row(table_metric, neo_m)

                max_rows = (
                    table_metric.row_count
                    if table_metric.row_count > max_rows
                    else max_rows
                )

            for neo_i in neos_imperial:

                self._add_new_row(table_imperial, neo_i)

                max_rows = (
                    table_imperial.row_count
                    if table_imperial.row_count > max_rows
                    else max_rows
                )

        self.notify("Data stored successfully!")

        final_height = 4 + (
            max_rows * 3
        )  # this value will be used as the ContentSwitcher height, otherwise when you get a shorter table the vertical scroll reset. +4 is for header and label

        self.switcher.styles.height = final_height

    def update_current(self) -> None:

        self.switcher.current = (
            self.ordered_days_list[self.day_index]
            if self.is_metric
            else f"{self.ordered_days_list[self.day_index]}_imperial"
        )

    def action_quit(self) -> None:

        self.exit()

    def action_toggle_units(self) -> None:

        self.is_metric = not self.is_metric

        self.update_current()

    def action_go_right(self) -> None:

        self.day_index = (self.day_index + 1) % len(self.ordered_days_list)

        self.update_current()

    def action_go_left(self) -> None:

        self.day_index = (self.day_index - 1) % len(self.ordered_days_list)

        self.update_current()
