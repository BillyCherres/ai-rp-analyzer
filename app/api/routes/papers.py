from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from sqlalchemy.orm import Session
from app.services.paper_service import get_db

from app.schemas.paper import PaperCreate, PaperResponse
from app.services.paper_service import createPaper, get_all_papers, get_paper_by_id

from typing import List

from app.services.pdf_service import extract_text_from_pdf


router = APIRouter()

@router.post("/papers", response_model=PaperResponse)
def create_paper_enpoint(paper: PaperCreate, db: Session = Depends(get_db)):
    return createPaper(paper, db)

@router.get("/papers", response_model=List[PaperResponse])
def get_papers_endpoint(db: Session = Depends(get_db)):
    return get_all_papers(db)

@router.get("/papers/{id}", response_model=PaperResponse)
def get_paper_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    paper = get_paper_by_id(id, db)
    
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")

    return paper

@router.post("/papers/upload", response_model=PaperResponse)
def post_paper(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    extracted_text = extract_text_from_pdf(file.file)
    
    if not extracted_text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    paper_data = PaperCreate(
        title = file.filename.replace(".pdf", ""),
        authors= [],
        abstract= "",
        content= extracted_text
    )
    
    created_paper = createPaper(paper_data, db)
    
    return created_paper

