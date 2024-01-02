import pymongo
from dotenv import load_dotenv
import os
# imSport colorlog

# logger = colorlog.getLogger('main-logger')
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
HADITH_DB_NAME = "hadithDB"

def get_client():
	try:
		client = pymongo.MongoClient(MONGO_URL)
	except Exception as e:
		logger.error("Error connecting to MongoDB")
		raise e		
	return client

client = get_client()
hadith_db = client.get_database(HADITH_DB_NAME)