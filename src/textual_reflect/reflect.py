#!/usr/bin/env python

import sys
from code import InteractiveConsole
from io import StringIO
from random import choice

from rich.syntax import Syntax
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import Footer, Header, RichLog, TextArea


class Reflector(Widget):
    BINDINGS = [
        ("ctrl+r", "eval", "eval"),
        ("ctrl+n", "dir", "namespace"),
        ("ctrl+l", "clear_output", "clear output"),
        ("ctrl+s", "clear_input", "clear input"),
    ]

    def compose(self) -> ComposeResult:
        self.input = TextArea.code_editor(
            id="reflector-input",
            language="python",
            placeholder="Press ^r to evaluate...",
        )
        self.input_container = Container(self.input, id="reflector-input-container")
        self.output = RichLog(id="reflector-output", markup=True, highlight=True)
        self.output_container = Container(self.output, id="reflector-output-container")

        yield self.output_container
        yield self.input_container

    def on_mount(self) -> None:
        self.input_container.border_title = "Input"
        self.output_container.border_title = "Output"
        self.namespace = {"app": self.app, "__builtins__": __builtins__}
        self.repl = InteractiveConsole(locals=self.namespace)
        self.input.focus()

    def action_dir(self) -> None:
        self.action_eval("dir()")

    def action_clear_output(self) -> None:
        self.output.clear()

    def action_clear_input(self) -> None:
        self.input.clear()

    def action_eval(self, code="") -> None:
        if not code:
            code = self.input.text
            if not code:
                return

        split_code = code.split("\n")
        self.output.write(Syntax(f">>> {split_code[0]}", "python", indent_guides=True))

        if len(split_code) > 1:
            for line in split_code[1:]:
                self.output.write(Syntax(f"... {line}", "python", indent_guides=True))
            self.output.write(Syntax("... ", "python", indent_guides=True))

        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = StringIO(), StringIO()
        self.repl.push(code + "\n")
        captured_output = sys.stdout.getvalue().strip()
        captured_error = sys.stderr.getvalue().strip()

        if captured_output:
            self.output.write(Syntax(captured_output, "python", indent_guides=True))
        if captured_error:
            self.output.write(Syntax(captured_error, "python", indent_guides=True))

        sys.stdout, sys.stderr = old_stdout, old_stderr
        self.input.clear()
        self.input.focus()


class ReflectorApp(App):
    CSS = """
    #reflector-input {
        padding: 1 2 1 2;
        border: none;
        background: $surface;
    }
    
    #reflector-output {
        padding: 1 2 1 2;
        background: $panel;
    }
    
    #reflector-input-container {
        border: solid $primary;
        height: 0.4fr;
        margin: 0 2 1 2;
        background: $background;
    }
    
    #reflector-input-container:focus-within {
        border: solid $accent;
    }
    
    #reflector-output-container {
        border: solid $primary;
        margin: 1 2 1 2;
        height: 0.6fr;
        background: $background;
    }
    """

    BINDINGS = [("ctrl+t", "toggle_theme", "toggle theme")]

    def compose(self) -> ComposeResult:
        self.header = Header(id="header", icon="🐍")
        self.reflector = Reflector(id="reflector")
        self.footer = Footer(id="footer")

        yield self.header
        yield self.reflector
        yield self.footer

    def on_mount(self) -> None:
        self.sub_title = "ReflectorWidget"
        self.theme = "monokai"
        self.reflector.input.theme = "monokai"

    def action_toggle_theme(self) -> None:
        themes = ["dracula", "monokai"]
        theme = "dracula" if self.theme == "monokai" else "monokai"
        self.theme = theme
        self.reflector.input.theme = theme
