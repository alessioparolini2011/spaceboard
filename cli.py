from textual.app import App, ComposeResult

from textual.widgets import Footer, Label

from textual.containers import Center


class spaceboard(App):

    BINDINGS = [("e", "exit", "Close the program")]

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

        yield Footer()

    def action_exit(self) -> None:

        self.exit()


if __name__ == "__main__":

    app = spaceboard()

    app.run()