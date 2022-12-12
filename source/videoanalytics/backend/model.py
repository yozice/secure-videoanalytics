"""Represents a basic inference model."""

from typing import Any, List, Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class InferenceModel(Protocol):
    """Basic representation of a inference model."""

    def load(self) -> None:
        """Load model in memory, initialize weights and cold run"""

    def unload(self) -> None:
        """Clear used memory"""

    def predict(self, image: np.ndarray) -> List[Any]:  # type: ignore
        """predict video stream"""
