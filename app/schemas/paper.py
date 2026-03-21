# pydantic validators. PaperCreate defines what the api accepts, PaperResponse defines what it sends back.

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
    chunks: List[str]