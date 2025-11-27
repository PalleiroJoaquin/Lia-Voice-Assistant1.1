"""
Skill implementations for lia_voice_assistant.

Each function in this module implements a distinct skill that the
assistant can perform in response to an intent. Skills return either
strings to be spoken or tuples ``(success, message)``. The
:func:`skill_router` function centralises dispatching based on intent
name.

Notes on specific skills:

* ``skill_greeting`` returns a simple greeting. In a future version you
  might vary responses or add contextual awareness.
* ``skill_time`` and ``skill_date`` use the local timezone and
  translate month and weekday names to Spanish.
* ``skill_dolar`` fetches exchange rates from the API URL provided via
  configuration. It returns the requested rate(s) or an error message
  if the request fails.
* ``skill_open_app`` looks up the program in the apps mapping loaded
  from :mod:`lia_voice_assistant.config`. It attempts to launch the
  executable and informs the user whether it succeeded.
"""

from __future__ import annotations

import datetime as _datetime
import subprocess
from typing import Dict, Tuple, Optional

import requests  # type: ignore

from .config import load_app_config, dolar_api_url


def skill_greeting() -> str:
    """Return a polite greeting."""
    return "Hola, ¿en qué puedo ayudarte hoy?"


def skill_time() -> str:
    """Return a string with the current time in 24‑hour format."""
    now = _datetime.datetime.now()
    return f"Son las {now:%H:%M} horas."


def skill_date() -> str:
    """Return a human‑readable date string in Spanish.

    Example: "Hoy es martes 11 de noviembre de 2025".
    """
    now = _datetime.datetime.now()
    weekdays = [
        "lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"
    ]
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ]
    weekday = weekdays[now.weekday()]
    month = months[now.month - 1]
    return f"Hoy es {weekday} {now.day} de {month} de {now.year}."


def _fetch_dolar_rates() -> Dict[str, float]:
    """Fetch dolar exchange rates from the configured API.

    Returns a mapping with keys ``oficial`` and ``blue``, each mapping
    to the sale price. Rates are floats representing pesos per USD.

    Raises
    ------
    requests.RequestException
        If the HTTP request fails or returns an unexpected status.
    KeyError
        If the JSON format differs from the expected structure.
    """
    response = requests.get(dolar_api_url(), timeout=5)
    response.raise_for_status()
    data = response.json()
    # The API returns a list of objects with names and prices
    rates: Dict[str, float] = {}
    for item in data:
        name = item.get("nombre", "").lower()
        price = item.get("venta")
        if name == "oficial":
            rates["oficial"] = float(price)
        elif name == "blue":
            rates["blue"] = float(price)
    return rates


def skill_dolar(which: Optional[str] = None) -> str:
    """Return the dolar exchange rate(s).

    Parameters
    ----------
    which:
        Optional specifier: ``"oficial"`` or ``"blue"``. If
        ``None``, both rates are returned.

    Returns
    -------
    str
        A message with the requested rate(s) or an error description.
    """
    try:
        rates = _fetch_dolar_rates()
    except Exception:
        return "No pude obtener la cotización del dólar en este momento."

    if which:
        rate = rates.get(which)
        if rate is None:
            return f"No reconozco la cotización '{which}'."
        return f"El dólar {which} está a {rate:.2f} pesos."
    # Return both rates
    parts = []
    for key in ["oficial", "blue"]:
        if key in rates:
            parts.append(f"{key}: {rates[key]:.2f} pesos")
    return "; ".join(parts)


def skill_open_app(name: str) -> Tuple[bool, str]:
    """Attempt to open an application configured in ``apps.yml``.

    Parameters
    ----------
    name:
        The program name as spoken by the user (lowercase). This is
        looked up in the application mapping loaded from
        :func:`lia_voice_assistant.config.load_app_config`.

    Returns
    -------
    (bool, str)
        Tuple ``(success, message)``. If ``success`` is ``True``, the
        application was launched; otherwise the message explains the
        error.
    """
    apps = load_app_config()
    cmd = apps.get(name)
    if not cmd:
        return False, f"No tengo configurado cómo abrir '{name}'."
    try:
        subprocess.Popen(cmd, shell=True)
    except Exception:
        return False, f"Hubo un problema al intentar abrir {name}."
    return True, f"Abriendo {name}."


def skill_goodbye() -> str:
    """Return a farewell message."""
    return "Hasta luego, ¡que tengas un buen día!"


def skill_router(intent: str, info: Dict[str, str]) -> Tuple[bool, str]:
    """Route an intent to the appropriate skill.

    Parameters
    ----------
    intent:
        Name of the intent as returned by
        :func:`lia_voice_assistant.intents.parse_intent`.
    info:
        Dictionary of captured values associated with the intent.

    Returns
    -------
    (bool, str)
        Tuple ``(speak, message)``. If ``speak`` is ``True``, the
        message should be spoken aloud. If ``False``, the assistant
        should return the message silently. For example, opening an
        application might not need to be spoken.
    """
    if intent == "greeting":
        return True, skill_greeting()
    if intent == "time":
        return True, skill_time()
    if intent == "date":
        return True, skill_date()
    if intent == "dolar":
        which = info.get("which") or None
        return True, skill_dolar(which)
    if intent == "open_app":
        success, msg = skill_open_app(info.get("name", ""))
        # Speak the result whether or not it succeeded
        return True, msg
    if intent == "goodbye":
        return True, skill_goodbye()
    return True, "No entendí tu pedido."


__all__ = [
    "skill_greeting",
    "skill_time",
    "skill_date",
    "skill_dolar",
    "skill_open_app",
    "skill_goodbye",
    "skill_router",
]