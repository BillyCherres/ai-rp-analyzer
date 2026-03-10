from fastapi import APIRouter, HTTPException

from app.schemas.paper import PaperCreate, PaperResponse
from app.services.paper_service import createPaper, get_all_papers, get_paper_by_id

from typing import List


router = APIRouter()

@router.post("/papers", response_model=PaperResponse)
def create_paper_enpoint(paper: PaperCreate):
    return createPaper(paper)

@router.get("/papers", response_model=List[PaperResponse])
def get_papers_endpoint():
    return get_all_papers()

@router.get("/papers/{id}", response_model=PaperResponse)
def get_paper_by_id_endpoint(id: int):
    paper = get_paper_by_id(id)
    
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")

    return paper
