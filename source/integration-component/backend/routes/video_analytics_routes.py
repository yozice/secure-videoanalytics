from backend.token import token_required
from backend.video_api import VideoAnalyticsAPI
from flask import Blueprint, jsonify, request

video_api = VideoAnalyticsAPI()

video_analytics = Blueprint("video_analytics", __name__)


@video_analytics.route("/process_video_stream", methods=["POST"])
@token_required
def process_video_stream():
    payload = request.get_json()
    stream_URL = payload["URL"]
    video_api.pass_stream(stream_URL)
    return jsonify()
