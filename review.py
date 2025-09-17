from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./reviews.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

def get_reviews():
    db = SessionLocal()
    reviews = db.query(Review).all()
    db.close()
    return reviews

def add_review(message: str):
    db = SessionLocal()
    review = Review(message=message)
    db.add(review)
    db.commit()
    db.refresh(review)
    db.close()
    return review
