import numpy as np
import keras
from keras.preprocessing import image

class PredictionPipeline:
    def __init__(self, file_name):
        self.file_name = file_name

    def predict(self):
        model = keras.models.load_model("artifacts\\model_training\\trained_model.h5")

        test_image = image.load_img(self.file_name, target_size=(160, 160))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        predicted_label = model.predict(test_image)

        res = "Steak" if predicted_label >= 0 else "Pizza"

        return [{"image" : res}]