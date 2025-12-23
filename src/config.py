import os

from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_REGION_NAME = os.environ["AWS_REGION_NAME"]

MODEL_NAME = os.getenv("MODEL_NAME", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "8192"))
RECURSION_LIMIT = int(os.getenv("RECURSION_LIMIT", "200"))
