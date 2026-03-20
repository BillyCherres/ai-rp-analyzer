from app.schemas.paper import PaperCreate
from app.services.text_chuncker import chunk_text 
from sqlalchemy.orm import Session
from app.models.paper import Paper  
from app.database import SessionLocal 

from app.vector_store import get_collection                                                            
from app.services.embedding_service import embed_texts

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
    
    embeddings = embed_texts(chunkList)
    collection = get_collection()
    
    ids = [f"paper_{new_paper.id}_chunk_{i}" for i in range(len(chunkList))]  
    
    collection.add(
        ids=ids,
        embeddings = embeddings,
        documents=chunkList,
        metadatas=[{"paper_id": new_paper.id} for i in range(len(chunkList))]
    )
    
    return new_paper
    

def get_all_papers(db: Session) -> list[Paper]:
    return db.query(Paper).all()

def get_paper_by_id(paper_id: int, db: Session) -> Paper | None:
    return db.query(Paper).filter(Paper.id ==  paper_id).first()