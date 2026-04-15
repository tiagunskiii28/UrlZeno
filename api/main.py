from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UrlBase(BaseModel):
    longurl: str
    shorturl: str
    alias: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/urls/")
async def create_url(url: UrlBase, db: db_dependency):
    db_url = models.Urls(longurl=url.longurl, shorturl=url.shorturl, alias=url.alias)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

