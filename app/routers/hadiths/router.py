from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.auth import validate_token

from db.models.hadith import Hadith
from db.models.search import HadithSearch

from db.config import hadith_db
from db.search import search_hadith

router = APIRouter(
	prefix="/hadiths",
	tags=["hadiths"],
	dependencies=[Depends(validate_token)]
)


hadiths_collection = hadith_db["hadiths"]

@router.get("/{id}", response_model=Hadith)
async def get_hadith(id: str):
	hadith = hadiths_collection.find_one({"_id": id})
	if hadith:
		return jsonable_encoder(hadith)
	raise HTTPException(status_code=404, detail="Hadith not found")


@router.post("/search", response_model=List[Hadith])
async def search_hadiths(query_body: HadithSearch):
	res = search_hadith(query_body)
	return res