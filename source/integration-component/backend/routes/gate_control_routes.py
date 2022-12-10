from backend.gate_api import GateAPI
from flask import Flask

gate_api = GateAPI()


def open_gate():
    # pass seconds?
    gate_api.open_gate()


def close_gate():
    gate_api.close_gate()


def init_app(app: Flask):
    app.add_url_rule("/open_gate", "open_gate", open_gate, methods=["GET"])
    app.add_url_rule("/close_gate", "close_gate", close_gate, methods=["GET"])
