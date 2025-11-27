"""
Text-to-speech utilities for lia_voice_assistant.

This module provides a thin wrapper around :mod:`pyttsx3` to simplify
initializing a Spanish voice and speaking text. It exposes two
functions:

``init_tts``
    Initialize and configure a pyttsx3 engine with sensible defaults.
    You can customise the speech rate and language. By default, it
    selects the first available voice matching the requested language.

``say``
    Speak a phrase synchronously using a previously created engine.

Example usage::

    from lia_voice_assistant import tts

    engine = tts.init_tts(rate=150)
    tts.say("Hola, ¿cómo estás?", engine)

This module does not attempt to catch exceptions at runtime. If
initialization or speech fails (for example, due to missing audio
drivers), the caller should handle the exception appropriately.
"""

from __future__ import annotations

import pyttsx3
from typing import Optional


def init_tts(rate: int = 145, voice_lang: str = "es") -> pyttsx3.Engine:
    """Initialize a pyttsx3 engine.

    Parameters
    ----------
    rate:
        Speech rate in words per minute. Defaults to 145.
    voice_lang:
        Language code to select a voice. Only the first voice whose
        ``languages`` attribute contains the code (case-insensitive) is
        used. If no match is found, the engine's default voice is kept.

    Returns
    -------
    pyttsx3.Engine
        Configured speech synthesis engine.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)

    # Try to select a voice matching the requested language
    requested = voice_lang.lower()
    for voice in engine.getProperty("voices"):
        # voices.languages may include multiple codes; join them into one string
        langs = " ".join(voice.languages).lower() if voice.languages else ""
        if requested in langs:
            engine.setProperty("voice", voice.id)
            break
    return engine


def say(text: str, engine: pyttsx3.Engine) -> None:
    """Speak text synchronously using the given engine.

    This function queues the utterance and blocks until it finishes.

    Parameters
    ----------
    text:
        The sentence to speak. If empty, this function returns
        immediately.
    engine:
        An initialized pyttsx3 engine. The caller is responsible for
        cleaning up the engine when finished (there is no explicit
        termination method; just dereferencing will suffice).
    """
    if not text:
        return
    engine.say(text)
    engine.runAndWait()


__all__ = ["init_tts", "say"]