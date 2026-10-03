import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from pathlib import Path



class PredictionPipeline:
    def __init__(self,filename):
        self.filename =filename


    
    def predict(self):
        # load model
        model_path = Path(__file__).resolve().parents[3] / "artifacts" / "training" / "model.h5"
        model = load_model(model_path)

        imagename = self.filename
        test_image = image.load_img(imagename, target_size = (224,224))
        test_image = image.img_to_array(test_image) / 255.0
        test_image = np.expand_dims(test_image, axis = 0)
        result = np.argmax(model.predict(test_image, verbose=0), axis=1)
        print(result)

        if result[0] == 1:
            prediction = 'Tumor'
            return [{ "image" : prediction}]
        else:
            prediction = 'Normal'
            return [{ "image" : prediction}]