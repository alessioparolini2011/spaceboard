"""
cli.py
This file uses Textual for create and manage an interactive CLI.
"""

from rich.align import Align

from rich.text import Text

from textual.app import App, ComposeResult

from textual.widgets import Footer, Label, DataTable, ContentSwitcher

from textual.containers import Center

from textual import work

from client import neo_req


class MiddleTxt(Align):
    def __init__(self, text: str, height: int = 3):
        super().__init__(
            Text.from_markup(text, justify="center"),
            vertical="middle",
            height=height,
        )


class spaceboard(App):

    BINDINGS = [
        ("e", "exit", "Close the program"),
        ("c", "change_units", "Units: (Metric/Imperial)"),
        ("left", "move_prev", "Go left (use left arrow key)"),
        ("right", "move_next", "Go right (use right arrow key)"),
    ]

    CSS_PATH = "spaceboard.tcss"

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

    def make_table(self, tid: str) -> DataTable:

        table = DataTable(
            classes="neotab",
            id=tid,
            cursor_type="row",
            zebra_stripes=True,
            cell_padding=3,
        )

        return table

    def _add_new_row(self, table: DataTable, neo_obj):
        table.add_row(
            MiddleTxt(neo_obj.name),
            MiddleTxt(neo_obj.id),
            MiddleTxt(f"{neo_obj.diam:,.3f}"),
            MiddleTxt(f"{neo_obj.speed:,.3f}"),
            MiddleTxt(f"{neo_obj.dis:,.3f}"),
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

            yield Label(
                "This is [b]spaceboard[/b], a space weather dashboard to visualize NEO (Near Earth Objects) for current, previous and next day.\nIt was created by Alessio Parolini in September 2026 for Hack Club X NASA event [b]Stardance[/b].",
                id="des",
            )

        with ContentSwitcher(initial=list(self.dates_id.keys())[0]):

            for day_id in self.dates_id.keys():

                yield self.make_table(day_id)

                yield self.make_table(f"{day_id}_imperial")

        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:

        self.data_update(self.api)

    @work(thread=True)
    def data_update(self, api) -> None:

        limit_days = (list(self.dates_id.keys())[-2], list(self.dates_id.keys())[-1])

        metric, imperial = neo_req(
            api,
            start_day=self.dates_id[limit_days[0]][0][0],
            end_day=self.dates_id[limit_days[1]][0][0],
        )

        if metric and imperial:

            self.call_from_thread(self.notify, "Datas achived successfully!")

        self.neo_by_unit["metric"] = metric

        self.neo_by_unit["imperial"] = imperial

        self.call_from_thread(self._store_data)

    def _store_data(self):

        for key in self.dates_id:
            self.dates_id[key][1] = (
                self.query_one(f"#{key}", DataTable),
                self.query_one(f"#{key}_imperial", DataTable),
            )

        for (target_date,), (table_metric, table_imperial) in self.dates_id.values():

            table_metric.add_columns(*self.COLUMNS_METRIC)

            table_imperial.add_columns(*self.COLUMNS_IMPERIAL)

            neos_metric = [
                n for n in self.neo_by_unit["metric"] if n.date == target_date
            ]

            neos_imperial = [
                n for n in self.neo_by_unit["imperial"] if n.date == target_date
            ]

            for neo_m in neos_metric:

                self._add_new_row(table_metric, neo_m)

            for neo_i in neos_imperial:

                self._add_new_row(table_imperial, neo_i)

        self.notify("Data stored successfully!")

    def action_exit(self) -> None:

        self.exit()

    def update_current(self) -> None:

        switcher = self.query_one(ContentSwitcher)

        switcher.current = (
            self.ordered_days_list[self.day_index]
            if self.is_metric
            else f"{self.ordered_days_list[self.day_index]}_imperial"
        )

    def action_change_units(self) -> None:

        self.is_metric = not self.is_metric

        self.update_current()

    def action_move_next(self) -> None:

        self.day_index = (self.day_index + 1) % len(self.ordered_days_list)

        self.update_current()

    def action_move_prev(self) -> None:

        self.day_index = (self.day_index - 1) % len(self.ordered_days_list)

        self.update_current()
