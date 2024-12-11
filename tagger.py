import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from constants import IMAGE_TAGGER_MODEL_PATH, IMAGE_TAGGER_TOKENIZER_PATH

class Tagger:
    _instance = None
    model = None
    tokenizer = None
    vocab_size = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Tagger, cls).__new__(cls)
            cls.model = load_model(IMAGE_TAGGER_MODEL_PATH)
            with open(IMAGE_TAGGER_TOKENIZER_PATH, 'r', encoding='utf-8') as f:
                tokenizer_json = f.read()
                cls.tokenizer = tokenizer_from_json(tokenizer_json)
                cls.vocab_size = len(cls.tokenizer.word_index)+1

        return cls._instance
    
    def generate_desc(self, image_path):
        photo = load_img(image_path, target_size=(512, 512))
        photo = img_to_array(photo)
        photo = np.expand_dims(photo, axis=0)
        photo = preprocess_input(photo)

        sequence = [self.tokenizer.word_index['start']]
        sequence_input = np.array([sequence[-1]])
        result = np.argmax(self.model.predict([photo, sequence_input], verbose=0), axis=-1)
        return [self.tokenizer.index_word.get(token) for token in filter(None, result[0])]