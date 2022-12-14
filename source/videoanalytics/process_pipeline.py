import argparse
import ast
import json
import logging
import os
import socket
import sys
import time
from datetime import datetime
from typing import Any, Optional

import cv2
import imagezmq
import requests
from backend.model import InferenceModel
from dotenv import load_dotenv

load_dotenv(".env")

sys.path.append("")

from backend.model_utils import load_models

models: dict[str, InferenceModel] = load_models()


def draw_prediction(frame, predictions):
    """
    Draws prediction rectangles and labels on frame image
    """
    for prediction in predictions:
        bbox = prediction["bbox"]
        label = prediction["label"]
        x1 = int(bbox[0] * frame.shape[1])
        y1 = int(bbox[1] * frame.shape[0])

        x2 = int(bbox[2] * frame.shape[1])
        y2 = int(bbox[3] * frame.shape[0])
        # draw bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # draw label
        cv2.rectangle(
            frame,
            (x1, y1 - int(25 / frame.shape[1])),
            (x2, y1),
            (0, 0, 255),
            cv2.FILLED,
        )
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(
            frame,
            label,
            (x1 + int(6 / frame.shape[0]), y1 - int(6 / frame.shape[1])),
            font,
            0.5,
            (255, 255, 255),
            1,
        )


def collect_detection_object(url, predictions) -> dict:
    """
    Collects object despribing result of frame processing
    """
    result = {}
    result["stream_id"] = url
    result["timestamp"] = datetime.now().strftime("%Y%m%d-%H%M%S")
    result["predictions"] = predictions
    return result


def process_pipeline(url: str, port: int):
    """
    Processing video stream from URL

    Streams proceeded output to given port
    """
    sender = imagezmq.ImageSender(
        connect_to=f"{os.environ['OUTPUT_STREAM_TCP']}:{port}", REQ_REP=False
    )
    rpi_name = socket.gethostname()  # send RPi hostname with each image
    # cap = cv2.VideoCapture(url)
    # cap.set(3, 500)
    # cap.set(4, 500)
    receiver = imagezmq.ImageHub(open_port=url, REQ_REP=False)
    # picam = VideoStream(usePiCamera=True).start()
    # time.sleep(2.0)  # allow camera sensor to warm up
    # camera = cv2.VideoCapture(url)
    # isSuccess, frame = camera.read()
    cam_name, frame = receiver.recv_image()
    # jpg = cv2.imencode(".jpg", frame)[1]
    while True:
        # Capture frame-by-frame
        cam_name, frame = receiver.recv_image()
        # jpg = cv2.imencode(".jpg", frame)[1]
        # read not succeeded
        if not cam_name:
            # break
            receiver = imagezmq.ImageHub(open_port=url, REQ_REP=False)
            cam_name, frame = receiver.recv_image()

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # face_prediction = models["face_recognition"].predict(frame)
        car_prediction = models["anpr_model"].predict(frame)

        # draw_prediction(frame, face_prediction)

        draw_prediction(frame, car_prediction)

        # Display the resulting frame
        sender.send_image(rpi_name, frame)

        # request to integration component
        # total_pred = face_prediction + car_prediction
        # total_pred = car_prediction

        # detection_obj = collect_detection_object(url, total_pred)

        # post_add_detection_request(detection_obj)

    # When everything is done, release the capture
    # camera.release()


def post_add_detection_request(detection_obj):
    """
    Sends post request to integration component to add detection information
    """
    try:
        requests.post(
            f"http://{os.environ['INTEGRATION_COMPONENT_URI']}/add_detection",
            json=json.dumps(detection_obj),
            timeout=1,
        )
    except requests.exceptions.ReadTimeout:
        pass


def parse_list_arg(str_arg: str):
    "Parses string to a list object"
    return ast.literal_eval(str_arg)


def get_log_path(logginq_required: bool) -> Optional[str]:
    "Returns path for logging in file if required"
    if not logginq_required:
        return None

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    filename = f"{os.environ['LOGS_FOLDER_PATH']}/{timestamp}.log"

    return filename


def _create_pipeline_parser() -> argparse.ArgumentParser:
    "Returns parser for process_pipeline"
    parser = argparse.ArgumentParser(description="pipiline information")
    parser.add_argument("-u", "--url", type=str, help="stream url")
    parser.add_argument("-p", "--port", type=int, help="port to output stream")
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

    process_pipeline(args.url, args.port)
