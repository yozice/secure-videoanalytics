import requests
from backend.models import VideoStream
from backend.token import token_required
from config import Config
from flask import Blueprint, jsonify, make_response, request
from global_variables import db

video_stream_bp = Blueprint("video_stream", __name__)


@video_stream_bp.route("/add_video_stream", methods=["POST"])
@token_required
def add_video_stream():
    data = request.get_json()
    video_stream = VideoStream.query.filter_by(name=data["name"]).first()
    if not video_stream:
        new_stream = VideoStream(name=data["name"], url=data["url"])
        resp = requests.post(
            f"{Config.VIDEO_ANALYTICS_URI}/predict_stream", json={"url": data["url"]}
        )
        new_stream.port = resp.json()["port"]
        db.session.add(new_stream)
        db.session.commit()
        return jsonify({"message": "registered successfully"}), 201
    else:
        return make_response(jsonify({"message": "video stream already exists"}), 409)


@video_stream_bp.route("/get_video_streams", methods=["GET"])
@token_required
def get_video_streams():
    vs_meta = VideoStream.query.all()
    vs_names = [x.name for x in vs_meta]
    return jsonify({"names": vs_names})


@video_stream_bp.route("/get_video_stream_info/<video_stream_name>", methods=["GET"])
@token_required
def get_video_stream_info(video_stream_name):
    vs = VideoStream.query.filter_by(name=video_stream_name).first()
    if vs:
        return jsonify({"id": vs.id, "name": vs.name, "url": vs.url})
    else:
        return make_response(jsonify({"message": "video stream does not exist"}), 409)


@video_stream_bp.route(
    "/get_video_detection_stream_uri/<video_stream_name>", methods=["GET"]
)
@token_required
def get_video_detection_stream_uri(video_stream_name):
    vs = VideoStream.query.filter_by(name=video_stream_name).first()
    if vs:
        return jsonify({"uri": f"tcp://0.0.0.0:{vs.port}"})
    else:
        return make_response(jsonify({"message": "video stream does not exist"}), 409)


@video_stream_bp.route("/rm_video_stream/<id>", methods=["DELETE"])
@token_required
def rm_video_stream(id):
    data = request.get_json()
    vs = VideoStream.query.filter_by(id=int(id)).delete()
    if vs:
        db.session.commit()
        return jsonify({"message": "successfully removed from database"}), 201
    else:
        return make_response(jsonify({"message": "video stream does not exist"}), 409)
