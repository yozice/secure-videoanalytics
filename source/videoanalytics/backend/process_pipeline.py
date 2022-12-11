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

load_dotenv("source/videoanalytics/.env")


sys.path.append("source/videoanalytics")

from backend import factory, loader


def draw_prediction(frame, prediction):
    for bbox, label in zip(prediction["bbox"], prediction["label"]):
        x1 = int(bbox[0] * frame.shape[0])
        y1 = int(bbox[1] * frame.shape[1])

        x2 = int(bbox[2] * frame.shape[0])
        y2 = int(bbox[3] * frame.shape[1])
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


def process_pipeline(url: str, port: str):
    sender = imagezmq.ImageSender(connect_to="tcp://0.0.0.0:5556", REQ_REP=False)
    rpi_name = socket.gethostname()  # send RPi hostname with each image
    cap = cv2.VideoCapture("http://192.168.1.3:4747/mjpegfeed?640x480")
    cap.set(3, 500)
    cap.set(4, 500)
    # picam = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)  # allow camera sensor to warm up

    # initialize models
    models = {}
    initialize_models(models)

    camera = cv2.VideoCapture(url)

    while True:
        # Capture frame-by-frame
        isSuccess, frame = camera.read()

        # break somehow
        if not isSuccess:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_prediction = models["face_recognizer"].predict(frame)

        draw_prediction(frame, face_prediction)

        # Draw a rectangle around the faces
        # for bbox, label in zip(prediction["bbox"], prediction["label"]):
        #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        #     cv2.rectangle(frame, (x1, y1 - 25), (x2, y1), (0, 0, 255), cv2.FILLED)
        #     font = cv2.FONT_HERSHEY_DUPLEX
        #     cv2.putText(frame, label, (x1 + 6, y1 - 6), font, 0.5, (255, 255, 255), 1)

        car_prediction = models["reg_num_recognizer"].predict(frame)

        draw_prediction(frame, car_prediction)

        # Draw a rectangle around the regestration numbers
        # for (x1, y1, x2, y2) in reg_nums:
        #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        #     cv2.rectangle(frame, (x1, y1 - 25), (x2, y1), (0, 255, 0), cv2.FILLED)
        #     font = cv2.FONT_HERSHEY_DUPLEX
        #     cv2.putText(frame, name, (x1 + 6, y1 - 6), font, 0.5, (0, 0, 0), 1)

        # Display the resulting frame
        # want to write to stream

        # request to integration component
        sender.send_image(rpi_name, frame)

    # When everything is done, release the capture
    camera.release()


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
