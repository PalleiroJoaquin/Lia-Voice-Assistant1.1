"""
Command‑line interface for lia_voice_assistant.

This module uses :mod:`typer` to expose convenient commands for
interacting with the assistant. The default command runs the
interactive loop defined in :func:`lia_voice_assistant.assistant.run`.
Additional commands may be added in the future (e.g. testing ASR,
listing configured applications, etc.).

Usage:

    python -m lia_voice_assistant           # start assistant
    python -m lia_voice_assistant assistant  # same as above
"""

from __future__ import annotations

import typer

from .assistant import run


app = typer.Typer(add_completion=False, help="Lía Voice Assistant CLI")


@app.command()
def assistant() -> None:
    """Run the interactive assistant loop."""
    run()


def main() -> None:
    """Entry point for ``python -m lia_voice_assistant``."""
    app()


if __name__ == "__main__":  # pragma: no cover
    main()