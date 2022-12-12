import json
import socket
import subprocess
from contextlib import closing

import psutil
from exceptions import InvalidPort
from global_variables import subprocess_dict


def create_subprocess(request) -> subprocess.Popen:
    """
    Creates pipeline subprocess
    """
    sp = subprocess.Popen(
        request,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return sp


def create_pipeline_request(script_path: str, url: str, port: int):
    """
    Creates request for subprocessing pipeline
    """
    request = [
        "python",
        script_path,
        "-u",
        url,
        "-p",
        port,
        # "-l",
    ]
    return request


def kill_subprocess(port: int) -> str:
    """
    Kills subprocess with given port

    Returns success message if process was killed or status code of process else
    """
    proc = subprocess_dict.get(port)
    if not proc:
        raise InvalidPort(port)

    proc.terminate()
    proc.wait()
    del subprocess_dict[port]
    try:
        status = psutil.Process(port).status()
    except psutil.NoSuchProcess:
        return "success"
    return status


def get_open_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def initialize_models():
    models = {}
    "Initializes models in models dict"
    with open(os.environ["MODELS_CONFIG_FILE"], "r", encoding="utf-8") as file:
        data = json.load(file)

    loader.load_plugins(data["plugins"])
    for item in data["models"]:
        if item["type"] not in models:
            models[item["type"]] = factory.create(item)
            models[item["type"]].load()
