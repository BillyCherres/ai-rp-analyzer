# defines the papers table in sqlite. each instance of this class is a row in the table.
from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    authors = Column(JSON)
    abstract = Column(String)
    content = Column(String)
    chunks = Column(JSON)
