"""Entry point for ``python -m lia_voice_assistant``.

This module simply forwards execution to the :mod:`lia_voice_assistant.cli`
command line interface. Running ``python -m lia_voice_assistant`` is
equivalent to executing ``python -m lia_voice_assistant.cli`` or
invoking the ``assistant`` command directly.
"""

from __future__ import annotations

from .cli import main


if __name__ == "__main__":  # pragma: no cover
    main()