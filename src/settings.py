import os

from dotenv import load_dotenv


load_dotenv()


AWS_PROFILE = os.getenv("AWS_PROFILE", "fake-auditor")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

