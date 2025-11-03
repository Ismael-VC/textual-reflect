"""Entry point for running the Textual ReflectorApp as a module."""

from .reflect import ReflectorApp

if __name__ == "__main__":
    app = ReflectorApp()
    app.run()
