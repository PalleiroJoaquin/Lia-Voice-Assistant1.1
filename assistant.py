"""
Top‑level assistant runner for lia_voice_assistant.

This module coordinates the different components of the assistant:
text‑to‑speech, automatic speech recognition, intent detection and
skill execution. It exposes a single :func:`run` function which starts
an interactive session on the terminal.

The assistant will greet the user, listen for utterances, parse their
intent and respond accordingly. If the user says goodbye, the
assistant exits the loop. Exceptions raised by ASR or TTS are
propagated to the caller to allow custom handling (e.g. logging or
graceful shutdown).

Example usage from the command line::

    from lia_voice_assistant.assistant import run
    run()

Alternatively, run ``python -m lia_voice_assistant`` to invoke the
Typer CLI defined in ``lia_voice_assistant.cli``.
"""

from __future__ import annotations

from .tts import init_tts, say
from .asr import transcribe_blocking
from .intents import parse_intent
from .skills import skill_router


def run() -> None:
    """Start the interactive voice assistant loop.

    The assistant greets the user, listens for voice input, detects the
    intent and dispatches to the appropriate skill. It speaks the
    response or prints it if speech synthesis fails. Saying goodbye
    ends the loop.
    """
    engine = init_tts()
    # Greet the user once at startup
    initial_message = "Hola, soy tu asistente. Estoy escuchando..."
    try:
        say(initial_message, engine)
    except Exception:
        print(initial_message)

    while True:
        # Record and transcribe speech
        try:
            text = transcribe_blocking()
        except Exception as exc:
            print(f"Error al grabar o transcribir: {exc}")
            continue
        if not text:
            continue
        intent, info = parse_intent(text)
        speak, response = skill_router(intent, info)
        if response:
            if speak:
                try:
                    say(response, engine)
                except Exception:
                    print(response)
            else:
                print(response)
        # Exit on goodbye
        if intent == "goodbye":
            break

    



__all__ = ["run"]