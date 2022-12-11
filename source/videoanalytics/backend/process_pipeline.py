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
from dotenv import load_dotenv
from imutils.video import VideoStream

load_dotenv("source/videoanalytics/.env")


sys.path.append("source/videoanalytics")


from backend import factory, loader


def gen_frames(camera):
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (
                b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )  # concat frame one by one and show result


def process_pipeline(url: str):
    # initialize models
    models = {}
    initialize_models(models)

    camera = cv2.VideoCapture(url)
    """
    for ip camera use 
        rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
    for local webcam use 
        cv2.VideoCapture(0)
    """

    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        prediction = models["face_recognizer"].predict(frame)

        # Draw a rectangle around the faces
        for bbox, label in zip(prediction["bbox"], prediction["label"]):
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.rectangle(frame, (x1, y1 - 25), (x2, y1), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, label, (x1 + 6, y1 - 6), font, 0.5, (255, 255, 255), 1)

        reg_nums = models["reg_num_recognizer"].predict(frame)

        # Draw a rectangle around the regestration numbers
        for (x1, y1, x2, y2) in reg_nums:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.rectangle(frame, (x1, y1 - 25), (x2, y1), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (x1 + 6, y1 - 6), font, 0.5, (0, 0, 0), 1)

        # Display the resulting frame
        # want to write to stream

        # request to integration component

        # break somehow
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # When everything is done, release the capture
    camera.release()
    # cv2.destroyAllWindows()


def initialize_models(models):
    "Initializes models in models dict"
    with open(os.environ["MODELS_CONFIG_FILE"], "r", encoding="utf-8") as file:
        data = json.load(file)

    loader.load_plugins(data["plugins"])
    for item in data["models"]:
        if item["type"] not in models:
            models[item["type"]] = factory.create(item)


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

    process_pipeline(args.url)
