import json

with open("configs.json", "r", encoding="utf-8") as f:
    CONFIGS = json.load(f)

BOT_TOKEN = CONFIGS["bot_token"]
IMAGE_TAGGER_MODEL_PATH = CONFIGS["model_path"]
IMAGE_TAGGER_TOKENIZER_PATH = CONFIGS["tokenizer_path"]
PERSISTENCE_PATH = CONFIGS["persistence_path"]
CONV_NAME = CONFIGS["conv_name"]
TOP_PATH = CONFIGS["top_path"]