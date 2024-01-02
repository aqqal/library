from fastapi import FastAPI

from app.logger import logger
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Aqqal Library of Works Service",
    description="API service for Aqqal chatbot, Aqqalbot",
)
