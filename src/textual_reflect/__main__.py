"""Entry point for running the Textual ReflectorApp as a module."""

from .reflect import Reflector

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header, Static


class ReflectorApp(App):
    CSS = """
        #reflector-container {
            height: 1fr;
        }
        
        #content {
            background: teal;
            height: 1fr;
        }
    """
    
    BINDINGS = [
        ("ctrl+t", "toggle", "toggle"),
    ]
    
    def compose(self) -> ComposeResult:
        self.header = Header(id="header", icon="🐍")
        self.reflector = Reflector(id="reflector")
        self.footer = Footer(id="footer")

        yield self.header
        yield Container(self.reflector, Container(), id="content")
        yield self.footer

    def action_toggle(self) -> None: 
        self.reflector.toggle()

    def on_mount(self) -> None:
        self.title = "Reflector"
        self.sub_title = "Demo"
        self.theme = "monokai"
        self.reflector.input.theme = "monokai"


if __name__ == "__main__":
    app = ReflectorApp()
    app.run()
