from db.models.hadith import HadithNarrator, Hadith
from fastapi.encoders import jsonable_encoder
from db.config import hadith_db

import pandas as pd
import json
import numpy as np


hadiths_collection = hadith_db["hadiths"]
narrators_collection = hadith_db["narrators"]

# chain gap exception
class ChainGapException(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


def parse_narrator(narrator_dict) -> HadithNarrator:
	"""Parse a narrator dictionary into a HadithNarrator object"""
	
	for k, v in narrator_dict.items():
		if not isinstance(v, str) and not isinstance(v, int):
			narrator_dict[k] = None
	

	narrator_dict["_id"] = str(narrator_dict["narrator_id"])

	if isinstance(narrator_dict["places_of_stay"], str):
		narrator_dict["places_of_stay"] = narrator_dict["places_of_stay"].split(",")
		narrator_dict["places_of_stay"] = [place.strip() for place in narrator_dict["places_of_stay"]]
	else:
		narrator_dict["places_of_stay"] = None

	narrator = HadithNarrator(**narrator_dict)
	
	return narrator


def populate_narrators_collection(collection, narrators_df: pd.DataFrame):
	"""
	Adds narrators to the database from dataframe and
	stores narrator documents in json file by narrator_id
	"""

	narrators_list = [] # used to append all to db
	narrators_dict = dict() # used to store each narrator by narrator_id in json file

	narrators_df_list = narrators_df.to_dict("records")

	for narrator_dict in narrators_df_list:
		
		# validate as HadithNarrator
		narrator = parse_narrator(narrator_dict)
		narrator_dict = jsonable_encoder(narrator, by_alias=True)

		narrators_list.append(narrator_dict)
		narrators_dict[narrator.id] = narrator_dict
		

	narrators_collection.insert_many(narrators_list)
	
	with open("narrators.json", "w") as f:
		json.dump(narrators_dict, f)


def inject_chain_with_narrators(hadith_dict: dict, narrators_dict: dict, reverse=True) -> dict:
	"""
	Populates the chain key in hadith dict with a list of narrator documents from narrators_dict
	"""

	narrators = hadith_dict.pop("chain")

	# get list of id strings from single comma seperated string
	narrators = [nid.strip() for nid in narrators.split(",")]
	
	if reverse:
		narrators = narrators[::-1]
	
	narrators_dicts = []

	for nid in narrators:
		if nid not in narrators_dict:
			raise ChainGapException(f"Narrator with id {nid} not found in narrators.json")
		
		# validate
		HadithNarrator(**narrators_dict.get(nid))
		narrators_dicts.append(narrators_dict.get(nid))

	hadith_dict["chain"] = narrators_dicts


def parse_hadith(hadith_dict: dict, narrators_dict: dict) -> Hadith:
	"""Parse a hadith dictionary into a Hadith object"""
	
	for k, v in hadith_dict.items():
		if not isinstance(v, str) and not isinstance(v, int):
			hadith_dict[k] = None

	hadith_dict["_id"] = str(hadith_dict["hadith_no"])

	try:
		# inject narrators
		inject_chain_with_narrators(hadith_dict, narrators_dict=narrators_dict)
		hadith_dict["top_narrator"] = hadith_dict["chain"][0]["name_en"]
	except ChainGapException as e:
		hadith_dict["chain"] = None
		hadith_dict["top_narrator"] = None

	# validate
	hadith = Hadith(**hadith_dict)
	return hadith_dict


def populate_hadiths_collection(collection, hadiths_df: pd.DataFrame):
	"""
	Adds a narrator to the database,
	"""

	hadiths_list = []  # used to append all to db
	hadiths_df_list = hadiths_df.to_dict("records")
	narrators_dict = json.load(open("narrators.json"))

	for hadith_dict in hadiths_df_list:

		# create and validate as Hadith object
		hadith = parse_hadith(hadith_dict, narrators_dict=narrators_dict)
		hadith_dict = jsonable_encoder(hadith, by_alias=True)
		hadiths_list.append(hadith_dict)
	
	hadiths_collection.insert_many(hadiths_list)

if __name__ == "__main__":
	narrators_df = pd.read_csv("../data/complete_narrators_clean.csv")
	populate_narrators_collection(narrators_collection, narrators_df)

	hadiths_df = pd.read_csv("../data/complete_hadiths_clean.csv").drop(columns=["id"], axis=1)
	populate_hadiths_collection(hadiths_collection, hadiths_df)