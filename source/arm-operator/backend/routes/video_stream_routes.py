import json

import cv2
import imagezmq
import requests
from backend.utils.request_utils import get_common_headers
from flask import Blueprint, Response, jsonify, make_response, render_template, request
from flask_login import current_user, login_required
from global_variables import Config, db

video_stream = Blueprint("video_stream", __name__)


@video_stream.route("/add_video_stream", methods=["POST"])
@login_required
def add_video_stream():
    data = request.get_json()  # {"name": .., "url": ..}
    resp = requests.post(
        f"{Config.IC_URI}/add_video_stream", headers=get_common_headers(), json=data
    )
    if resp:
        return jsonify({"message": resp.json()["message"]}), 201
    else:
        return make_response(jsonify({"message": resp.json()["message"]}), 409)


@video_stream.route("/get_video_stream_info/<video_stream_name>", methods=["GET"])
@login_required
def get_video_stream_info(video_stream_name):
    vs_info = requests.get(
        f"{Config.IC_URI}/get_video_stream_info", headers=get_common_headers()
    ).json()

    if vs_info:
        return jsonify(
            {"id": vs_info["id"], "name": vs_info["name"], "url": vs_info["url"]}
        )
    else:
        return make_response(jsonify({"message": "video stream does not exist"}), 409)


@video_stream.route("/rm_video_stream/<id>", methods=["DELETE"])
@login_required
def rm_video_stream(id):
    resp = requests.delete(
        f"{Config.IC_URI}/rm_video_stream/{id}",
        headers=get_common_headers(),
    )
    if resp:
        return jsonify(resp.json()), 201
    else:
        return make_response(jsonify({"message": resp.json()["message"]}), 409)


@video_stream.route("/online_stream/<video_stream_name>", methods=["GET"])
@login_required
def online_stream(video_stream_name):
    uri = requests.get(
        f"{Config.IC_URI}/get_video_detection_stream_uri/{video_stream_name}",
        headers=get_common_headers(),
    ).json()["uri"]
    return Response(
        sendImagesToWeb(uri), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


def sendImagesToWeb(uri):
    receiver = imagezmq.ImageHub(open_port=uri, REQ_REP=False)
    while True:
        camName, frame = receiver.recv_image()
        jpg = cv2.imencode(".jpg", frame)[1]
        yield b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + jpg.tostring() + b"\r\n"
