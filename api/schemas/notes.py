from enum import Enum
from typing import List
from pydantic import BaseModel
from datetime import datetime
from api.schemas.base import BaseResponse


class Categoty(str, Enum):
    HOME = "Home"
    WORK = "Work"
    PERSONAL = "Personal"

class NoteData(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime
    category: Categoty
    user_id: str

class NoteResponse(BaseResponse):
    data: NoteData

class NoteListResponse(BaseResponse):
    data: List[NoteData]