from pathlib import Path
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.image import load_img, img_to_array

from image_tagger.exceptions import WrongFileFormatError

class Tagger:
    model_path = None
    tokenizer_path = None
    _instance = None
    _model = None
    _tokenizer = None
    _vocab_size = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Tagger, cls).__new__(cls)
        return cls._instance

    def load_model(self):
        self._model = load_model(self.model_path)
        with open(self.tokenizer_path, 'r', encoding='utf-8') as f:
            tokenizer_json = f.read()
        self._tokenizer = tokenizer_from_json(tokenizer_json)
        self._vocab_size = len(self._tokenizer.word_index)+1

    # def __setattr__(self, name, value):
    #     if name == "model_path":
    #         if isinstance(value, str):
    #             value = Path(value)
    #         if not value.exists():
    #             raise FileNotFoundError("Model file not found")
    #         try:
    #             self._model = load_model(value)
    #             #TODO: добавить проверку на модель
    #         except Exception:
    #             raise WrongFileFormatError("Model file is not a keras model")
        
    #     elif name == "tokenizer_path":
    #         if isinstance(value, str):
    #             value = Path(value)
    #         if not value.exists():
    #             raise FileNotFoundError("Model file not found")
    #         try:
    #             with open(value, 'r', encoding='utf-8') as f:
    #                 tokenizer_json = f.read()
    #                 print(f"File content: {tokenizer_json[:100]}...")  # Печатаем первые 100 символов
    #                 self._tokenizer = tokenizer_from_json(tokenizer_json)
    #                 print(self._tokenizer.word_index)
    #                 self.vocab_size = len(self._tokenizer.word_index)+1
    #         except Exception as e:
    #             print(e)
    #             raise WrongFileFormatError("Tokenizer file is not a JSON")

    def generate_desc(self, image_path: str) -> list[str]:
        if self._model is None:
            raise RuntimeError("Model is not loaded")
        if self._tokenizer is None:
            raise RuntimeError("Tokenizer is not loaded")
        photo = load_img(image_path, target_size=(512, 512))
        photo = img_to_array(photo)
        photo = np.expand_dims(photo, axis=0)
        photo = preprocess_input(photo)

        sequence = [self._tokenizer.word_index['start']]
        sequence_input = np.array([sequence[-1]])
        result = np.argmax(self._model.predict([photo, sequence_input], verbose=0), axis=-1)
        return [self._tokenizer.index_word.get(token) for token in filter(None, result[0])]