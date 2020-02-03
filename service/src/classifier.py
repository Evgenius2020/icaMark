import numpy as np
from keras.preprocessing.image import img_to_array, load_img
from keras.models import model_from_json


class Classifier:
    def __init__(self):
        with open('cnn_struct.json', 'r') as json_file:
            loaded_model_json = json_file.read()
        cnn = model_from_json(loaded_model_json)
        cnn.load_weights("cnn_weights.h5")
        print("Loaded model from disk")
        self.cnn = cnn

    def get_label(self, plot_filename):
        # loading image
        img = load_img(plot_filename)
        img.thumbnail((180, 176))
        x = img_to_array(img)
        x = (x - 128.0) / 128.0
        dataset = np.ndarray(shape=(1, 176, 180, 3), dtype=np.float32)
        dataset[0] = x

        # getting cnn prediction
        return int(self.cnn.predict_classes(dataset)[0][0])
