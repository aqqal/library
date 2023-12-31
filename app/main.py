from fastapi import FastAPI, APIRouter
from app.logger import logger

from app.routers.hadiths.router import router as hadiths_router
from app.routers.semantic_search.router import router as semantic_search_router

from dotenv import load_dotenv
from config import log_config

import uvicorn

load_dotenv()

app = FastAPI(
    title="Aqqal Library of Works Service",
    description="Includes hadiths, Narrators, and hadith semantic search",
    version="0.1.0",
)

library_router = APIRouter(
    prefix="/library",
)

library_router.include_router(hadiths_router)
library_router.include_router(semantic_search_router)

app.include_router(library_router)
# uvicorn.run(app=app, log_config=log_config)