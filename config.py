"""
Configuration utilities for lia_voice_assistant.

This module centralizes loading of environment variables and application
configuration used by the voice assistant. It loads values from a
``.env`` file if present (via :mod:`dotenv`) and reads the optional
``apps.yml`` file to map spoken application names to system commands.

To add or change application mappings, create an ``apps.yml`` file next to
your project's entry point with content like::

    default:
      navegador: "C:/Program Files/Google/Chrome/Application/chrome.exe"
      editor: "code"

If the file is missing or unreadable, the assistant will still start
but the ``open_app`` skill will return an informative message.

The following environment variables are recognized:

``VOSK_MODEL``
    Path to a Vosk speech recognition model. If unset, the ASR module
    will attempt to download a Spanish model automatically the first
    time it is used. See :mod:`lia_voice_assistant.asr` for details.
``DOLAR_API``
    URL of an API returning JSON with keys ``venta`` and ``compra``.
    The default is set to consult Blue and official rates from the
    ``dolarapi.com`` service.
``MAX_BLOCK_SECONDS``
    Maximum duration (in seconds) to record a single utterance when
    listening for voice input. Defaults to ``5`` seconds.

The :func:`load_app_config` function returns a dictionary mapping spoken
names to executable commands, merging the ``default`` profile with the
profile corresponding to the current machine's hostname when available.
"""

from __future__ import annotations

import os
import socket
from pathlib import Path
from typing import Dict

import yaml
from dotenv import load_dotenv

# Load variables from .env file if present
load_dotenv()

def get_env(key: str, default: str | int | None = None) -> str | int | None:
    """Return the value of an environment variable or a default.

    Environment variables are case-sensitive. If the variable is not set
    or is empty, ``default`` is returned.
    """
    value = os.getenv(key)
    return value if value else default


def max_block_seconds() -> int:
    """Return the maximum duration to record audio blocks in seconds.

    Falls back to 5 seconds if the ``MAX_BLOCK_SECONDS`` environment
    variable is not defined.
    """
    try:
        return int(get_env("MAX_BLOCK_SECONDS", 5))
    except ValueError:
        return 5


def load_app_config(config_path: str | Path = "apps.yml") -> Dict[str, str]:
    """Load application mappings from a YAML file.

    The configuration file may define multiple profiles. A ``default``
    profile should always be present. If another profile matching the
    machine's hostname exists, its values override those in
    ``default``. Missing files or YAML errors are silently ignored and
    result in an empty mapping.

    Parameters
    ----------
    config_path:
        Path to the YAML configuration file. Defaults to ``apps.yml``.

    Returns
    -------
    dict
        Mapping of spoken names to executable commands.
    """
    config_file = Path(config_path)
    if not config_file.exists():
        return {}

    try:
        with config_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except yaml.YAMLError:
        return {}

    hostname = socket.gethostname().lower()
    default_mapping = data.get("default", {})
    host_mapping = data.get(hostname, {})
    # Host-specific values override defaults
    return {**default_mapping, **host_mapping}


def dolar_api_url() -> str:
    """Return the URL used to fetch dolar exchange rates.

    The default API endpoint returns Blue and official rates from
    ``dolarapi.com``. Users can override this via the ``DOLAR_API``
    environment variable.
    """
    return str(get_env("DOLAR_API", "https://dolarapi.com/v1/dolares"))


__all__ = [
    "get_env",
    "max_block_seconds",
    "load_app_config",
    "dolar_api_url",
]