from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.auth import validate_token

from db.models.hadith import Hadith, HadithNarrator
from db.models.search import HadithSearch, NarratorSearch

from db.config import hadith_db
from db.search import hadiths_search, narrators_search

router = APIRouter(
	prefix="/hadiths",
	tags=["hadiths"],
	dependencies=[Depends(validate_token)]
)


hadiths_collection = hadith_db["hadiths"]
narrators_collection = hadith_db["narrators"]


@router.get("/", response_model=List[Hadith])
async def get_hadiths(limit: int = 10, skip: int = 0, include_chains: bool = True):
	proj = {"chain": 0} if not include_chains else {}

	hadiths = hadiths_collection.find({}, proj).skip(skip).limit(limit)
	return jsonable_encoder(hadiths)


@router.post("/search", response_model=List[Hadith])
async def search_hadiths(body: HadithSearch, skip: int = 0, limit: int = 10, include_chains: bool = False):
	res = hadiths_search(body, limit, skip, include_chains)
	return res


@router.get("/narrators", response_model=List[HadithNarrator])
async def get_narrators(limit: int = 10, skip: int = 0):
	res = narrators_collection.find().skip(skip).limit(limit)
	return res


@router.post("/narrators/search", response_model=List[HadithNarrator])
async def search_narrators(body: NarratorSearch, limit: int = 10, skip: int = 0):
	res = narrators_search(body, limit, skip)
	return res


@router.get("/narrators/{id}", response_model=HadithNarrator)
async def get_narrator(id: str):
	narrator = narrators_collection.find_one({"_id": id})
	if narrator:
		return jsonable_encoder(narrator)
	
	raise HTTPException(status_code=404, detail="Narrator not found")


@router.get("/{id}", response_model=Hadith)
async def get_hadith(id: str, include_chain: bool = True):
	proj = {"chain": 0} if not include_chains else {}
	
	hadith = hadiths_collection.find_one({"_id": id}, proj)
	if hadith:
		return hadith
	raise HTTPException(status_code=404, detail="Hadith not found")