from detection.detector import Detector
from recognition.recognizer import Recognizer


class Model:
    def __init__(self):
        self.detector = Detector()
        self.recognizer = Recognizer()

    def load(self):
        self.detector.load()
        self.recognizer.load()

    def predict(self, img):
        coords = self.detector.predict(img)
        h, w = img.shape[0], img.shape[1]

        preds = [
            {
                "type": "auto",
                "bbox": coord,
                "label": self.recognizer.predict(
                    img[
                        int(coord[1] * h) : int(coord[3] * h),
                        int(coord[0] * w) : int(coord[2] * w),
                    ]
                )[0],
            }
            for coord in coords
        ]

        return preds
