from app.schemas.paper import PaperCreate, PaperResponse

papers_db: list[PaperResponse] = []
next_id = 1

def createPaper(paper_data: PaperCreate) -> PaperResponse:
    global next_id
    
    new_paper = PaperResponse(
        id=next_id,
        title=paper_data.title,
        authors=paper_data.authors,
        abstract=paper_data.abstract,
        content=paper_data.content,
    )
    
    papers_db.append(new_paper)
    next_id += 1
    
    return new_paper

def get_all_papers() -> list[PaperResponse]:
    return papers_db

def get_paper_by_id(paper_id: int) -> PaperResponse | None:
    for paper in papers_db:
        if paper.id == paper_id:
            return paper
        
    return None