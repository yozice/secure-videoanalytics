import argparse
import ast
import json
import logging
import os
import sys
import time
from datetime import datetime
from typing import Any, Optional

sys.path.append("source")


from backend import factory, loader
from backend.common.pipeline_utils import create_pipeline, exec_pipeline


def process_pipeline(plugin_names: list[str], class_ids: list[Any], path_src: str):
    """
    Processes pipeline request

    --------------------------
    Input:
        * plugin_names - list of model names
        * class_ids - list of classes to predict for each model
        * path_src - path to directory
    """
    # create pipeline
    pipeline = create_pipeline(plugin_names, class_ids)

    # get list of image names
    try:
        filenames = list_images(
            os.path.normpath(f"{app_configuration.DATA_FOLDER}/{path_src}")
        )
    except FileNotFoundError as exc:
        logging.error(exc)
        return str(exc)

    # initialize models
    models = {}
    initialize_models(models, plugin_names)

    # exec pipeline
    timestamp = datetime.utcnow()

    for pipe_el in pipeline:
        exec_pipeline(pipe_el, filenames, models, timestamp)

    logging.info("pipeline processed")


def initialize_models(models, plugin_names: list[str]):
    "Initializes models in models dict"
    with open(app_configuration.MODELS_CONFIG_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    loader.load_plugins(data["plugins"])
    for item in data["models"]:
        if item["type"] not in models and item["type"] in plugin_names:
            models[item["type"]] = factory.create(item)


def parse_list_arg(str_arg: str):
    "Parses string to a list object"
    return ast.literal_eval(str_arg)


def get_log_path(logginq_required: bool) -> Optional[str]:
    "Returns path for logging in file if required"
    if not logginq_required:
        return None

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    filename = f"{app_configuration.LOGS_FOLDER_PATH}/{timestamp}.log"

    return filename


def _create_pipeline_parser() -> argparse.ArgumentParser:
    "Returns parser for process_pipeline"
    parser = argparse.ArgumentParser(description="pipiline information")
    parser.add_argument("-u", "--url", type=str, help="stream url")
    parser.add_argument(
        "-l",
        "--log",
        action=argparse.BooleanOptionalAction,
        help="use to write logs to file",
    )
    return parser


if __name__ == "__main__":
    parser = _create_pipeline_parser()
    args = parser.parse_args()

    log_filename = get_log_path(args.log)

    logging.basicConfig(
        level=logging.INFO,
        filename=log_filename,
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
    )

    start_time = time.time()

    process_pipeline(args.plugin_names, args.class_ids, args.path_src)

    logging.info("--- %s seconds ---", (time.time() - start_time))
