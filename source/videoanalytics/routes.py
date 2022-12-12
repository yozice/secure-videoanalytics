import os

from flask import Blueprint, Response, jsonify, render_template, request

from backend.subprocess_utils import (
    create_pipeline_request,
    create_subprocess,
    get_open_port,
    kill_subprocess,
)
from global_variables import subprocess_dict

app = Blueprint("analytics", __name__)


@app.route("/predict_stream", methods=["POST"])
def predict_stream():
    # get video stream url
    url = request.get_json()["url"]
    port = str(get_open_port())

    pipeline_req = create_pipeline_request(
        os.environ["PROCESS_PIPELINE_SCRIPT_PATH"], url, port
    )

    proc = create_subprocess(pipeline_req)
    subprocess_dict[port] = proc
    return jsonify({"port": port})


@app.route("/kill_process")
def kill_process():
    "Kills process with given PID"
    port = int(request.form.get("port"))  # type: ignore
    message = kill_subprocess(port)
    return jsonify(message)
