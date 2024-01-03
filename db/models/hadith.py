from pydantic import BaseModel, Field
from typing import Optional, List


class HadithNarrator(BaseModel):
	class Config:
		pupulate_by_name = True

	id: str = Field(..., alias="_id")
	"""_id is a string of the narrator_id used in database retrieval and routing"""

	narrator_id: int
	grade: Optional[str]
	"""The grade of the narrator in terms of generations. E.x: Companion, Tabi'"""

	name_en: Optional[str]
	"""The name of the narrator in English"""

	name_ar: Optional[str]
	"""The name of the narrator in Arabic"""

	death_reason: Optional[str]
	"""The reason of death of the narrator"""

	places_of_stay: Optional[List[str]] = None
	"""The places where the narrator stayed"""


class Hadith(BaseModel):
	class Config:
		populate_by_name = True

	id: str = Field(..., alias="_id")
	"""_id is a string of the hadith_no used in database retrieval and routing"""	
	
	hadith_no: int
	"""hadith_no is the number of the hadith in the book (Uncoordinated Refrence)"""

	book: Optional[str]
	"""The title of the book of hadith in which the hadith was reported"""

	chapter_en: Optional[str]
	"""The title of the chapter of the hadith in which the hadith was reported in English"""

	chapter_ar: Optional[str]
	"""The title of the chapter of the hadith in which the hadith was reported in Arabic"""

	text_en: Optional[str]
	"""The text of the hadith in English"""

	text_ar: Optional[str]
	"""The text of the hadith in Arabic"""

	top_narrator: Optional[str]
	"""The name of the top most narrator after Rasool Allah (SAW)"""

	chain: Optional[List[HadithNarrator]] = None
	"""
	The chain of narrators Sof the hadith, with the top most narrator after
	after Rasool Allah (SAW) being the first in the lisT
	"""