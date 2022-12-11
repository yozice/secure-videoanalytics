import os

from flask import Blueprint, Response, jsonify, render_template, request

from backend.subprocess_utils import (
    create_pipeline_request,
    create_subprocess,
    kill_subprocess,
)
from global_variables import subprocess_dict

app = Blueprint("analytics", __name__)


@app.route("/predict_stream")
def predict_stream():
    # get video stream url
    url = request.form.get("url")
    pipeline_req = create_pipeline_request(
        os.environ["PROCESS_PIPELINE_SCRIPT_PATH"], url
    )
    proc = create_subprocess(url)
    subprocess_dict[proc.pid] = proc
    return jsonify({"pid": proc.pid})


@app.route("/kill_process")
def kill_process():
    "Kills process with given PID"
    pid = request.form.get("pid")
    message = kill_subprocess(pid)
    return jsonify(message)
