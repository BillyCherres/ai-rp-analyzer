from app.schemas.paper import PaperCreate
from app.services.text_chuncker import chunk_text 
from sqlalchemy.orm import Session
from app.models.paper import Paper  
from app.database import SessionLocal 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def createPaper(paper_data: PaperCreate, db: Session) -> Paper:
    
    chunkList = chunk_text(paper_data.content)
    new_paper = Paper(
        title=paper_data.title,
        authors=paper_data.authors,
        abstract=paper_data.abstract,
        content=paper_data.content,
        chunks=chunkList
    )
    db.add(new_paper) 
    db.commit() 
    db.refresh(new_paper)
    
    return new_paper
    

def get_all_papers(db: Session) -> list[Paper]:
    return db.query(Paper).all()

def get_paper_by_id(paper_id: int, db: Session) -> Paper | None:
    return db.query(Paper).filter(Paper.id ==  paper_id).first()