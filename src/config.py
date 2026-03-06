import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 3