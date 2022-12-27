import torch
import numpy as np

IMG_SIZE = 512
NMS_THRESHOLD = 0.4
PREDICTION_THRESHOLD = 0.5
MODEL_YOLOv5_PATH = ""

class Yolov5Model:
    """Yolov5 model for object detection."""

    def __init__(self, model_path=MODEL_YOLOv5_PATH, img_size=IMG_SIZE, **kwargs):
        self.model = self.get_model(model_path, **kwargs)
        self.img_size = img_size

    def get_model(self, path=MODEL_YOLOv5_PATH):
        model = torch.hub.load(
            "ultralytics/yolov5", "custom", path=path, force_reload=True, _verbose=False
        )
        return model

    def predict(
        self, image, threshold=PREDICTION_THRESHOLD
    ):
        """Predict bounding boxes for image."""
        self.model.conf = NMS_THRESHOLD
        prediction = self.model(image, size=self.img_size)

        labels, cords = self.__get_bbox_data(prediction)
        cords = self.convert_bboxs(cords)
        prediction = self.merge_prediction(labels, cords)
        return prediction
    
    def convert_bboxs(self, cords):
      new_cords = torch.zeros(cords.shape)
      for idx, entry in enumerate(cords):
        new_cords[idx, :4] = entry[:4] * self.img_size
        new_cords[idx, 4:] = entry[4:]
      return new_cords

    def merge_prediction(self, labels, coords):
      entries = np.zeros((coords.shape[0], 6))
      for idx, (label, coord) in enumerate(zip(labels, coords)):
        entries[idx, 0] = label
        entries[idx, 1:] = coord
      return entries

    def __get_bbox_data(self, prediction):
        labels, cords = prediction.xyxyn[0][:, -1], prediction.xyxyn[0][:, :-1]
        return labels, cords