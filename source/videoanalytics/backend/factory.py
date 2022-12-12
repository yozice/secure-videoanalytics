"""Factory for creating model plugins."""

from typing import Any, Callable, Dict

from exceptions import UnknownModelType
from backend.model import InferenceModel

Factory = Dict[str, Callable[..., InferenceModel]]
model_creation_funcs: Factory = {}


def clear_factory():
    global model_creation_funcs
    model_creation_funcs = {}


def get_factory() -> Factory:
    return model_creation_funcs


def register(model_type: str, creator_fn: Callable[..., InferenceModel]) -> None:
    """Register a new inference model character type."""
    model_creation_funcs[model_type] = creator_fn


def unregister(model_type: str) -> None:
    """Unregister a inference model type."""
    model_creation_funcs.pop(model_type, None)


def create(arguments: Dict[str, Any]) -> InferenceModel:
    """Create a inference model of a specific type, given JSON data."""
    args_copy = arguments.copy()
    model_type = args_copy.pop("type")
    try:
        creator_func = model_creation_funcs[model_type]
    except KeyError:
        raise UnknownModelType(f"unknown model type {model_type!r}") from None
    return creator_func(**args_copy)
