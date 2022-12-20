from typing import Any, List

import numpy as np
from backend import factory

from .detection.detector import Detector
from .recognition.recognizer import Recognizer


class AnprModel:
    def __init__(self):
        self.detector = Detector()
        self.recognizer = Recognizer()

    def load(self):
        self.detector.load()
        self.recognizer.load()

    def unload(self):
        pass

    def predict(self, image: np.ndarray) -> List[Any]:
        coords = self.detector.predict(image)
        h, w = image.shape[0], image.shape[1]
        # if isinstance(coords, type(None)):
        preds = [
            {
                "type": "auto",
                "bbox": coord,
                "label": self.recognizer.predict(
                    image[
                        int(coord[1] * h) : int(coord[3] * h),
                        int(coord[0] * w) : int(coord[2] * w),
                    ]
                )[0],
            }
            for coord in coords
        ]
        # else:
        #     return []

        return preds


def register() -> None:
    factory.register("anpr_model", AnprModel)
