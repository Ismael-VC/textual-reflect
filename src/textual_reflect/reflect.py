#!/usr/bin/env python


from __future__ import annotations

import sys
from code import interact, InteractiveConsole
from io import StringIO
from typing import TYPE_CHECKING

from rich.syntax import Syntax
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import RichLog, TextArea

if TYPE_CHECKING:
    from typing_extensions import Self


class Reflector(Widget):
    # def __init__(self):
        # pass

    BINDINGS = [
        ("ctrl+r", "eval", "eval"),
        ("ctrl+n", "dir", "namespace"),
        ("ctrl+l", "clear_output", "clear output"),
        ("ctrl+s", "clear_input", "clear input"),
    ]
    
    DEFAULT_CSS = """
        #reflector-input {
            padding: 0 1 0 1;
            border: none;
            background: $surface;
        }

        #reflector-output {
            padding: 0 1 0 1;
            background: $surface;
        }

        #reflector-input-container {
            border: solid $primary;
            height: 0.4fr;
            margin: 0 1 0 1;
            background: $background;
        }

        #reflector-input-container:focus-within {
            border: solid $accent;
        }

        #reflector-output-container {
            border: solid $primary;
            margin: 0 1 0 1;
            height: 0.6fr;
            background: $background;
        }

        #reflector-container {
            border: solid $primary;
            background: $background;
            margin: 0 1 0 1;
        }
    """


    def compose(self) -> ComposeResult: 
        self.input = TextArea.code_editor(
            id="reflector-input",
            language="python",
            show_line_numbers=False,
            soft_wrap=True,
            placeholder="Press ^r to evaluate.",
        )
        
        self.input_container = Container(
            self.input, 
            id="reflector-input-container"
        )
        
        self.output = RichLog(
            id="reflector-output", 
            markup=True, 
            highlight=True,
            # min_width=80,
            # wrap=True
        )
        
        self.output_container = Container(
            self.output, 
            id="reflector-output-container"
        )
        
        self.container = Container(
            self.output_container, 
            self.input_container, 
            id="reflector-container"
        )

        yield self.container


    def on_mount(self) -> None:
        self.stdout, self.stderr = sys.stdout, sys.stderr
        self.more_input = False
        self.prompt = ">>> "
        self.input_container.border_title = f"{self.prompt}"
        self.output_container.border_title = f"{self.app.title}"
        self.input_container.border_subtitle = "Input"
        self.output_container.border_subtitle = "Output"
        self.namespace = {"app": self.app, "__builtins__": __builtins__}
        self.repl = InteractiveConsole(locals=self.namespace)
        self.banner = f"""\
Python {sys.version} on {sys.platform}
Type "help", "copyright", "credits" or "license" for more information.
        """
        self.write(self.banner)
        self.input.focus()

    def action_dir(self) -> None:
        self.action_eval("dir()")

    def action_clear_output(self) -> None:
        self.output.clear()

    def action_clear_input(self) -> None:
        self.input.clear()

    def write(self, content:str="") -> Self:
        return self.output.write(Syntax(content, "python", indent_guides=True))

    def redirect_io(self):
        sys.stdout, sys.stderr = StringIO(), StringIO()

    def restore_io(self):
        sys.stdout, sys.stderr = self.stdout, self.stderr
    
    def action_eval(self, code="", capture=False) -> Tuple[str, str]|None:
        if not code:
            code = self.input.text

        for line in code.split("\n"):
            self.write(f"{self.prompt}{line}")
            self.redirect_io()
            self.more_input = self.repl.push(line)  
            captured_output = sys.stdout.getvalue().strip()
            captured_error = sys.stderr.getvalue().strip()
            self.restore_io()

            if captured_output:
                self.write(captured_output)
    
            if captured_error:
                self.write(captured_error)

            if self.more_input:
                self.prompt = "... "
                # self.input_container.styles.border = ("solid", "yellow")
            else:
                self.prompt = ">>> "
                # self.input_container.styles.border = self.accent

            self.input_container.border_title = f"{self.prompt}"

            self.input.clear()
            self.input.focus()

            if capture:
                return captured_output, captured_error     
