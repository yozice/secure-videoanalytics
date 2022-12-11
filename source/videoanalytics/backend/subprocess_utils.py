import json
import subprocess

import psutil
from exceptions import InvalidPID
from global_variables import subprocess_dict


def create_subprocess(request) -> subprocess.Popen:
    """
    Creates pipeline subprocess

    ---------------------------
    Input:
        * script_path - path to subprocess entry point
        * data - parametrs to be passed to subprocess script

    Returns:
        * subprocess.Popen object
    """
    sp = subprocess.Popen(
        request,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return sp


def create_pipeline_request(script_path: str, url):
    """
    Creates request for subprocessing pipeline
    """

    request = [
        "python",
        script_path,
        "-u",
        json.dumps(url),
        # "-l",
    ]
    return request


def kill_subprocess(pid: int) -> str:
    """
    Kills subprocess with given PID

    Returns success message if process was killed or status code of process else
    """
    proc = subprocess_dict.get(pid)
    if not proc:
        raise InvalidPID(pid)

    proc.terminate()
    proc.wait()
    del subprocess_dict[pid]
    try:
        status = psutil.Process(pid).status()
    except psutil.NoSuchProcess:
        return "success"
    return status
