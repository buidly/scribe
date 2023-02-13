from __future__ import annotations

from enum import Enum
from typing import Any, Callable

from . import settings


class EnvironmentType(Enum):
    DEVNET = "devnet"
    TESTNET = "testnet"
    MAINNET = "mainnet"
    TEST = "test"

    def load_config(self) -> None:
        """Based on the input environment, load the configuration"""
        mapping: dict[EnvironmentType, Callable[..., Any]] = {
            EnvironmentType.DEVNET: settings.load_devnet,
            EnvironmentType.TESTNET: settings.load_testnet,
            EnvironmentType.TEST: settings.load_test_config,
        }

        mapping[self]()
