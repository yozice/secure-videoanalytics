import json
import os

from backend import factory, loader
from backend.model import InferenceModel


def load_models():
    "Loads models in models dict"
    models = {}
    with open(os.environ["MODELS_CONFIG_FILE"], "r", encoding="utf-8") as file:
        data = json.load(file)

    loader.load_plugins(data["plugins"])
    for item in data["models"]:
        if item["type"] not in models:
            models[item["type"]] = factory.create(item)
            models[item["type"]].load()

    return models


models: dict[str, InferenceModel] = load_models()

# {port: subprocess.Popen}
subprocess_dict = {}
