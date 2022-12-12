from typing import List, Optional, Tuple

import cv2
import numpy as np
import torch
from .utils import non_max_suppression, normalize


class Detector:
    def __init__(
        self,
        weights_path: str = "./detection/weights/weights.torchscript",
        input_image_shape: Tuple[int, int] = (640, 640),
        input_image_channels: int = 3,
        batch_size: int = 10,
        detector_labels: Optional[List[str]] = None,
    ) -> None:
        self.model_type = "detector"

        self.model = None
        self.device = (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        self.loaded = False
        self.input_image_shape = input_image_shape
        self.input_image_channels = input_image_channels
        self.batch_size = batch_size
        self.weights_path = weights_path

        if detector_labels is None:
            self.detector_labels = ["plate"]
        else:
            self.detector_labels = detector_labels

    def load(self):
        if not self.loaded:
            self.model = torch.jit.load(self.weights_path, map_location=self.device)
            self.model.eval()
            self.loaded = True

    def unload(self):
        del self.model
        self.model = None
        self.loaded = False

    def preprocess(
        self, images: List[np.ndarray], input_image_shape: Tuple[int, int]
    ) -> torch.Tensor:
        resized = [
            cv2.resize(
                image, tuple(input_image_shape[:2]), interpolation=cv2.INTER_CUBIC
            )
            for image in images
        ]
        tensor = np.array(resized)
        tensor = tensor.astype(np.float32)
        tensor /= 255
        return torch.Tensor(tensor)

    def postprocess(
        self,
        predictions: torch.Tensor,
        width: int,
        height: int,
    ) -> List[list]:
        outputs = non_max_suppression(predictions)
        outputs = [normalize(output, (width, height)) for output in outputs]
        preds = [[i for i in output[..., :4].tolist()] for output in outputs]
        return preds[0]

    def predict(self, img):
        img = self.preprocess([img], self.input_image_shape)[0]
        img = img.unsqueeze(0)
        w, h = img.shape[-2], img.shape[-3]
        output = self._call_model(img)

        results = self.postprocess(output, w, h)

        return results

    def _call_model(self, images: torch.Tensor) -> torch.Tensor:
        if not self.loaded or isinstance(self.model, type(None)):
            raise Exception('Model is not loaded')
        batch = images.permute((0, -1, 1, 2)).to(self.device)
        images = batch.to(self.device)
        output = self.model(images)[0]
        return output
