from textual.app import App, ComposeResult

from textual.widgets import Footer, Header

class spaceboard(App):

    BINDINGS = [("d", "toogle_dark", "Toogle dark mode")]

    def compose(self) -> ComposeResult:

        yield Header()

        yield Footer()

    def action_toogle_dark(self) -> None:

        self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")


if __name__ == "__main__":

    app = spaceboard()

    app.run()