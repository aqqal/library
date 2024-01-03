from pydantic import BaseModel
from typing import Optional

class HadithSearch(BaseModel):
	"""
	Search for hadiths
	"""
	book: Optional[str] = None
	"""Query string for title of the book of hadith in which the hadith was reported"""

	text_en: Optional[str] = None
	"""Query string of the hadith text in English"""

	top_narrator: Optional[str] = None
	"""Query string of the name of the top most narrator in the sanad chain of the hadith"""