"""lia_voice_assistant package.

This package provides a modular, extensible voice assistant written in
Python. It combines speech recognition, text‑to‑speech synthesis,
intent detection and skill execution in a simple architecture. The
assistant currently understands a handful of Spanish commands such as
greetings, asking for the time or date, querying the dolar exchange
rate and opening configured applications.

Modules available include:

``config``
    Environment variable and application configuration utilities.
``tts``
    Text‑to‑speech (pyttsx3) wrapper functions.
``asr``
    Automatic speech recognition (Vosk) functions.
``intents``
    Regex‑based intent detection.
``skills``
    High level implementations for each supported intent.
``assistant``
    Coordination logic to run an interactive assistant session.
``cli``
    Command line interface powered by Typer.

At the package root, :func:`lia_voice_assistant.run` is provided as a
convenience to start the assistant from code.
"""

from __future__ import annotations

from .assistant import run

__all__ = ["run"]
