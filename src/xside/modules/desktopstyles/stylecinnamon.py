#!/usr/bin/env python3
import logging
import os
import pathlib
import sys

import xside.modules.color as color
import xside.modules.desktopstyles.stylegnome as stylegnome


class EnvStyleCinnamon(stylegnome.EnvStyleGnome):
    """..."""

    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
