import torch
import torchvision.transforms as transforms
from glob import glob
from typing import Tuple, Any, List, Optional, Dict
import os
import cv2
import numpy as np

from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image


class FaceRecognition:
    def __init__(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.detector = torch.load("models/detector.pt")
        self.recognizer = torch.load("models/recognizer.pt")
        self.classifier = torch.load("models/classifier.pt")
        self.margin = 20
        self.classifier_threshold = 0.98359
        self.recognizer_threshold = 0.5
        self.cosine = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
        self.to_tensor = transforms.Compose([transforms.PILToTensor()])
        self.classifier_trannsform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])
        self.recognizer_transform = transforms.Compose([
            transforms.Resize((160, 160)),
            transforms.ToTensor(),
        ])
        
        self.datadir = "data"
        self.infopath = "data/info.csv"
        
    def add_person(self, img: np.array, person_id: str):
        frame = Image.fromarray(img)
        img_cropped, prob = self.detector(frame, return_prob=True)
        if len(prob) == 0:
            return
        img_cropped = img_cropped[np.argmax(prob)]
        embedding = self.recognizer(img_cropped.unsqueeze(0).to(self.device)).detach().cpu()
        if len(embedding):
            person_dir = f"{self.datadir}/{person_id}"
            if not os.path.exists(person_dir):
                os.mkdir(person_dir)
            cv2.imwrite(f"{person_dir}/image.png", img)
            torch.save(embedding[0], f"{person_dir}/{person_id}.pt")

    def delete_person(self, person_id: str):
        person_dir = f"{self.datadir}/{person_id}"
        os.remove(f"{person_dir}/image.png")
        os.remove(f"{person_dir}/{person_id}.pt")
        os.rmdir(person_dir)
        
    def _get_embeddings(self) -> Dict[str, torch.tensor]:
        files = glob(f"{self.datadir}/**/*.pt", recursive=True)
        return {os.path.basename(file)[:-3]: torch.load(file) for file in files}
    
    def _get_label(self, e1: torch.tensor) -> str:
        embeddings = self._get_embeddings()
        max_name, max_val = "", -1
        for name, e2 in embeddings.items():
            cur_max = self.cosine(e1, e2).item()
            if cur_max > max_val:
                max_val = cur_max
                max_name = name
        return max_name if max_val > self.recognizer_threshold else "" 
    
    def _preprocess_data(self, img: np.array, model_type: str = "classifier") -> torch.tensor:
        processed_data = Image.fromarray(img)
        if model_type == "classifier":
            processed_data = self.classifier_trannsform(processed_data)
        else:
            processed_data = self.recognizer_transform(processed_data)
        return processed_data
    
    def predict(self, img: np.array) -> List[Dict[str, Any]]:
        h, w, _ = img.shape
        frame = Image.fromarray(img)
        bboxes, _ = self.detector.detect(frame)
        
        frame = self.to_tensor(frame)
        crops = []
        for bb in bboxes:
            xs, ys, xf, yf = [int(b) for b in bb]
            crops.append(self._preprocess_data(img[
                min(xs - self.margin, 0):min(xf + self.margin, w), 
                min(ys - self.margin, 0):min(yf + self.margin, h)
            ]))
 
        tensor_crops = []
        new_bboxes = []
        labels = []
        for i, prob in enumerate(self.classifier(crops).cpu().numpy()):
            if float(prob[1]) <= self.classifier_threshold:
                xs, ys, xf, yf = [int(b) for b in bboxes[i]]
                tensor_crops.append(
                    self._preprocess_data(img[xs:xf, ys:yf], "recognizer"))
                new_bboxes.append(bboxes[i])
        if len(tensor_crops):
            tensor_crops = torch.stack(tensor_crops).to(self.device)
            embeddings = self.recognizer(tensor_crops).detach().cpu()
            labels = [self._get_label(e) for e in embeddings]
    
        return [{
            "type": "face",
            "bbox": [bbox[0] / w, bbox[1] / h, bbox[2] / w, bbox[3] / h],
            "label": label
        } for bbox, label in zip(new_bboxes, labels)]
