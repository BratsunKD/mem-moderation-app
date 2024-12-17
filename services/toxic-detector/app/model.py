import time


class MockModel:
    def __init__(self, weights_path: str):
        print(f"Initializing model with weights from {weights_path}")
        self.weights_path = weights_path

    def predict(self, text: str) -> int:
        time.sleep(1)
        return len(text)