from pydantic import BaseModel
from typing import List

class PaperCreate(BaseModel):
    title: str
    authors: List[str]
    abstract: str
    content: str
    
class PaperResponse(BaseModel):
    id: int
    title: str
    authors: List[str]
    abstract: str
    content: str