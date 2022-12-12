import cv2
import numpy as np
import torch
from torch.autograd import Variable

from .model import build_lprnet


class Recognizer:

    CHARS = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "A",
        "B",
        "E",
        "K",
        "M",
        "H",
        "O",
        "P",
        "C",
        "T",
        "Y",
        "X",
    ]

    CHARS_DICT = {char: i for i, char in enumerate(CHARS)}

    def __init__(self):
        self.lpr_max_len = 9
        self.img_size = (94, 24)

    def load(self, weights_path="./recognition/weights/best.pth"):
        self.model = build_lprnet(
            lpr_max_len=self.lpr_max_len,
            phase=False,
            class_num=len(self.CHARS),
            dropout_rate=0.0,
        )
        self.weights_path = weights_path
        device = (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        self.model.to(device)
        self.model.load_state_dict(torch.load(self.weights_path))
        print("Successful to build network!")

    def transform(self, img):
        img = img.astype("float32")
        img -= 127.5
        img *= 0.0078125
        img = np.transpose(img, (2, 0, 1))
        return img

    def predict(self, frame):
        img = cv2.resize(frame, self.img_size)
        img = self.transform(img)
        img = np.expand_dims(img, axis=0)
        img = Variable(torch.tensor(img, dtype=torch.float).to("cuda"))

        prebs = self.model(img)
        prebs = prebs.cpu().detach().numpy()
        preb_labels = list()
        for i in range(prebs.shape[0]):
            preb = prebs[i, :, :]
            preb_label = list()
            for j in range(preb.shape[1]):
                preb_label.append(np.argmax(preb[:, j], axis=0))
            no_repeat_blank_label = list()
            pre_c = preb_label[0]
            if pre_c != len(self.CHARS) - 1:
                no_repeat_blank_label.append(pre_c)
            for c in preb_label:  # dropout repeate label and blank label
                if (pre_c == c) or (c == len(self.CHARS) - 1):
                    if c == len(self.CHARS) - 1:
                        pre_c = c
                    continue
                no_repeat_blank_label.append(c)
                pre_c = c
            preb_labels.append(no_repeat_blank_label)

        return ["".join(map(lambda x: self.CHARS[x], label)) for label in preb_labels]
