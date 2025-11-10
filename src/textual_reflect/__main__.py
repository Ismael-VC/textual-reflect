"""Entry point for running the Textual ReflectorApp as a module."""

from .reflect import Reflector

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class ReflectorApp(App):
    BINDINGS = [("ctrl+t", "toggle_theme", "toggle theme")]

    def compose(self) -> ComposeResult:
        self.header = Header(id="header", icon="🐍")
        self.reflector = Reflector(id="reflector")
        self.footer = Footer(id="footer")

        yield self.header
        yield self.reflector
        yield self.footer

    def on_mount(self) -> None:
        self.title = "Reflector"
        self.sub_title = "Demo"
        self.theme = "monokai"
        self.reflector.input.theme = "monokai"

    def action_toggle_theme(self) -> None:
        themes = ["dracula", "monokai"]
        theme = "dracula" if self.theme == "monokai" else "monokai"
        self.theme = theme
        self.reflector.input.theme = theme


if __name__ == "__main__":
    app = ReflectorApp()
    app.run()
