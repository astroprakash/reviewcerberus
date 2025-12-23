import boto3
from botocore.config import Config
from langchain.chat_models import init_chat_model

from ..config import (
    AWS_ACCESS_KEY_ID,
    AWS_REGION_NAME,
    AWS_SECRET_ACCESS_KEY,
    MAX_OUTPUT_TOKENS,
    MODEL_NAME,
)
from .caching_bedrock_client import CachingBedrockClient

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=AWS_REGION_NAME,
    endpoint_url=f"https://bedrock-runtime.{AWS_REGION_NAME}.amazonaws.com",
    config=Config(
        read_timeout=180.0,
        retries={
            "max_attempts": 3,
        },
    ),
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

caching_bedrock_client = CachingBedrockClient(bedrock_client)

model = init_chat_model(
    MODEL_NAME,
    client=caching_bedrock_client,
    model_provider="bedrock_converse",
    temperature=0.0,
    max_tokens=MAX_OUTPUT_TOKENS,
)
