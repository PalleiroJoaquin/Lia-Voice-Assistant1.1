"""
Intent detection for lia_voice_assistant.

This module defines a small set of regular expressions to detect user
intents from Spanish utterances. The :func:`parse_intent` function
iterates through these patterns in the order they are defined and
returns the first match along with any captured information. If no
pattern matches, it returns ``("unknown", {})``.

Intents currently supported:

``greeting``
    Salutations or phrases like "hola", "buen día", etc.
``time``
    Asking for the current time.
``date``
    Asking for the current date.
``dolar``
    Asking for the exchange rate; optional group ``which`` may be
    ``"oficial"`` or ``"blue"``. If absent, both are reported.
``open_app``
    Asking to open a program; captures the program name as ``name``.
``goodbye``
    Phrases indicating the conversation should end, like "chau" or
    "adiós".

If you extend the set of intents, remember to order more specific
patterns before more general ones to avoid false positives.
"""

from __future__ import annotations

import re
from typing import Dict, Tuple


INTENT_PATTERNS = [
    # Greeting should be detected early
    ("greeting", re.compile(r"\b(hola|buen(?:os|as)?\s*(?:d[ií]a|tardes?|noches?))\b", re.IGNORECASE)),
    ("time", re.compile(r"\b(qué\s*hora|hora)\b", re.IGNORECASE)),
    ("date", re.compile(r"\b(qué\s*d[ií]a|fecha)\b", re.IGNORECASE)),
    # Dolar with optional specifier
    ("dolar", re.compile(r"\b(?:d[oó]lar)\s*(?P<which>oficial|blue)?\b", re.IGNORECASE)),
    # Open application; captures program name
    ("open_app", re.compile(r"\b(?:abr(?:ir|e|í|e))\s+(?P<name>[\wñáéíóú]+)\b", re.IGNORECASE)),
    # Farewell
    ("goodbye", re.compile(r"\b(chau|ad[ií]os|hasta\s+luego)\b", re.IGNORECASE)),
]


def parse_intent(text: str) -> Tuple[str, Dict[str, str]]:
    """Determine the intent of the user's utterance.

    Parameters
    ----------
    text:
        Input sentence, already lower‑cased if desired. The function
        operates case‑insensitively.

    Returns
    -------
    (str, dict)
        A tuple ``(intent_name, info)`` where ``intent_name`` is one of
        the strings defined in ``INTENT_PATTERNS`` or ``"unknown"``,
        and ``info`` contains any named capture groups extracted from
        the pattern. Keys are as declared in the pattern (e.g.
        ``"which"``, ``"name"``).
    """
    for name, pattern in INTENT_PATTERNS:
        match = pattern.search(text)
        if match:
            # Normalize captured values to lowercase strings
            info = {k: (v.lower() if v is not None else v) for k, v in match.groupdict().items()}
            return name, info
    return "unknown", {}


__all__ = ["INTENT_PATTERNS", "parse_intent"]