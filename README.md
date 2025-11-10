# Textual Reflect

A Textual widget for inspecting Python code reflection.

## Installation

```bash
$ uv pip install textual-reflect
```

## Usage

```python
from textual.app import App, ComposeResult
from textual_reflect import Reflector

class MyApp(App):
    def compose(self) -> ComposeResult:
        yield Reflector()  # Add widget

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

TODO

- input accept empty string, write empty line, push \r
- use sys prompts and return value
- capture banner
- 1 big container
- force vertical
- vertical group?
- animation top down
- log not focusable
