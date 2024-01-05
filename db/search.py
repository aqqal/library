from typing import List

from db.config import hadith_db
from db.models.hadith import Hadith, HadithNarrator
from db.models.search import HadithSearch, NarratorSearch

from logger import logger

hadiths_collection = hadith_db["hadiths"]
narrators_collection = hadith_db["narrators"]

def hadiths_search(search_obj: HadithSearch, limit=10, skip=0, include_chains=False) -> List[Hadith]:
	"""
	Result strings are case insensitive using Atlas standard analyzer
	"""
	search_dict = search_obj.dict()
	has_query = False
	for key in search_dict:
		if search_dict[key]:
			has_query = True

	pipeline = [
		{ "$limit": limit }
	]
	

	proj = {
		"$project": {"chain": 0}
	}

	if not include_chains:
		pipeline.insert(0, proj)

	if skip > 0:
		pipeline.append({"$skip": skip})

	if has_query:
		pipeline.insert(0,
			{
				"$search": {
					"compound": {
					"should": get_should_clauses(search_dict)
					}
				},
			},
		)

	res = hadiths_collection.aggregate(pipeline)
	return res


def get_should_clauses(search_dict):
	"""
	Dynamically generates a list of should clauses 	
	"""
	book_ranking_clauses: list = [
		{
			"text": {
				"query": "sahih bukhari",
				"path": "book",
				"score": { "boost": { "value": 3 } }
			}
		},
		{
			"text": {
				"query": "sahih muslim",
				"path": "book",
				"score": { "boost": { "value": 2 } }
			}
		}
	]

	book_clause: dict = {
		"text": {
			"fuzzy" : {},
			"query": search_dict.get("book", ""),
			"path": "book",
			"score": { "boost": { "value": 4 } }
		}
	} if search_dict["book"] else None

	# give the most priority to book if specified
	if book_clause:	
		book_ranking_clauses.insert(0, book_clause)

	clauses = book_ranking_clauses

	top_narrator_clause: dict =  {
		"text":	{
			"fuzzy" : {},
			"query": search_dict.get("top_narrator", ""),
			"path": "top_narrator",
			"score": { "boost": { "value": 2.5 } }
		}
	} if search_dict["top_narrator"] else None

	if top_narrator_clause:
		clauses.append(top_narrator_clause)

	text_clause: dict = {
		"text": {
			"fuzzy" : {},
			"query": search_dict.get("text_en", ""),
			"path": "text_en"
		}
	} if search_dict["text_en"] else None

	if text_clause:
		clauses.append(text_clause)

	return clauses


def narrators_search(search_obj: NarratorSearch, limit=10, skip=0) -> List[HadithNarrator]:
	"""
	Result strings are case insensitive using Atlas standard analyzer
	"""
	search_dict = search_obj.dict()
	
	has_query = False
	for key in search_dict:
		if search_dict[key]:
			has_query = True

	pipeline = [
		{ "$limit": limit }
	]

	if skip > 0:
		pipeline.append({"$skip": skip})

	if has_query:
		pipeline.insert(0,
			{
				"$search": {
					"compound": {
					"should": [
							{
								"text": {
									"fuzzy" : {},
									"query": search_dict.get("name_en", ""),
									"path": "name_en"
								}
							},
							{
								"text": {
									"fuzzy": {},
									"query": "companion",
									"path": "grade",
									"score": { "boost": { "value": 2 } }
								}
							}
						]
					}
				},
			},
		)

	res = narrators_collection.aggregate(pipeline)
	return res
