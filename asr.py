"""
Automatic speech recognition utilities for lia_voice_assistant.

This module wraps :mod:`vosk` and :mod:`sounddevice` to perform simple
blocking speech recognition from the microphone. It provides two main
functions:

``get_model``
    Return a loaded Vosk model instance. The model path is taken from
    the ``VOSK_MODEL`` environment variable; if the variable is unset,
    it defaults to ``model`` relative to the current working
    directory. If the model directory does not exist, a
    :class:`RuntimeError` is raised explaining that the user needs to
    download a Spanish Vosk model and set the environment variable.

``transcribe_blocking``
    Record audio from the default microphone for up to ``max_seconds``
    and return the recognized text as a lower‑cased string. The
    function captures audio in 16 kHz, mono, 16‑bit little endian
    format, which is required by Vosk. If no speech is recognized, an
    empty string is returned.

These functions rely on external dependencies (``vosk``,
``sounddevice``, ``numpy``). They may raise exceptions if audio
recording fails, the model cannot be loaded, or the recognition
encountered an unexpected error. Caller code should handle these
exceptions gracefully.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

import numpy as np  # type: ignore
import sounddevice as sd  # type: ignore
import vosk  # type: ignore

from .config import get_env, max_block_seconds

_model: Optional[vosk.Model] = None


def get_model() -> vosk.Model:
    """Load and cache the Vosk model specified by the environment.

    Returns
    -------
    vosk.Model
        Loaded Vosk model ready for recognition.

    Raises
    ------
    RuntimeError
        If the model directory does not exist.
    """
    global _model
    if _model is not None:
        return _model

    model_path = Path(str(get_env("VOSK_MODEL", "model")))
    if not model_path.exists():
        raise RuntimeError(
            f"Vosk model not found at {model_path}. "
            "Please download a Spanish model (e.g. 'vosk-model-small-es-0.42') "
            "and set the VOSK_MODEL environment variable to its path."
        )
    _model = vosk.Model(str(model_path))
    return _model


def _record_audio(seconds: int) -> np.ndarray:
    """Record audio from the default microphone.

    Parameters
    ----------
    seconds:
        Maximum duration of the recording. Must be positive.

    Returns
    -------
    numpy.ndarray
        One-dimensional array of PCM samples (float32). Sample rate is
        fixed at 16 kHz.
    """
    sample_rate = 16000
    channels = 1
    sd.default.samplerate = sample_rate
    sd.default.channels = channels
    recording = sd.rec(int(seconds * sample_rate), dtype="float32")
    sd.wait()
    return recording.reshape(-1)


def transcribe_blocking(max_seconds: Optional[int] = None) -> str:
    """Record audio and return the recognized text.

    Parameters
    ----------
    max_seconds:
        Maximum length of the recording. If ``None`` (default), it
        falls back to the value returned by :func:`max_block_seconds`.

    Returns
    -------
    str
        Lower‑cased transcription of the recorded audio. Returns an
        empty string if nothing was recognized.
    """
    seconds = max_seconds or max_block_seconds()
    audio = _record_audio(seconds)
    recognizer = vosk.KaldiRecognizer(get_model(), 16000)
    # Convert float32 audio to int16 PCM
    int_audio = (audio * 32767).astype("int16").tobytes()
    recognizer.AcceptWaveform(int_audio)
    result = json.loads(recognizer.Result())
    return result.get("text", "").strip().lower()


__all__ = ["get_model", "transcribe_blocking"]