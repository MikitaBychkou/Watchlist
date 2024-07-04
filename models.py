from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mssql+pymssql://sa:Films1234!@localhost:1434"
engine = create_engine(DATABASE_URL)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    status = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    publication_year = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)

    def __repr__(self):
        return (f"Title: {self.title}, Director: {self.director}, Genre: {self.genre}, "
                f"Status: {self.status}, Rating: {self.rating}, "
                f"Publication Year: {self.publication_year}, Comments: {self.comments}")

Base.metadata.create_all(bind=engine)