from backend.video_api import VideoAnalyticsAPI
from flask import Flask, jsonify, render_template, request

video_api = VideoAnalyticsAPI()


def process_video_stream():
    payload = request.get_json()
    stream_URL = payload["URL"]
    video_api.pass_stream(stream_URL)


def init_app(app: Flask):
    app.add_url_rule(
        "/process_video_stream",
        "process_video_stream",
        process_video_stream,
        methods=["POST"],
    )
