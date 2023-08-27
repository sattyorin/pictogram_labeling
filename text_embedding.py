import os
from typing import Optional

import openai
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding

EMBEDDING_MODEL = "text-embedding-ada-002"


class TextEmbedding:
    def __init__(self):
        execution_dir_path = os.path.dirname(os.path.abspath(__file__))
        load_dotenv(dotenv_path=os.path.join(execution_dir_path, ".env"))
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def do_embedding(self, text: str) -> Optional[str]:
        if not text:
            return None
        return get_embedding(text, engine=EMBEDDING_MODEL)
