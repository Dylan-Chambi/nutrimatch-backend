from abc import ABC


class GeneralFoodDetector(ABC):
    def __init__(self, model, model_name):
        self.model_name = model_name
        self.model = model

    def detect_food(self, image_b64: str):
        pass