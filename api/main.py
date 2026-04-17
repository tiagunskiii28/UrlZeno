from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
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

class ShortUrlUpdate(BaseModel):
    shorturl: str

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

@app.get("/{shorturl}")
async def get_url(shorturl: str, db: Session = Depends(get_db)):
    url = db.query(models.Urls).filter(models.Urls.shorturl == shorturl).first()

    if url is None:
        raise HTTPException(status_code = 404, detail = "URL No Encontrada")
    return RedirectResponse(url=url.longurl, status_code=302)

@app.delete("/urls/{shorturl}")
async def delete_url(shorturl: str, db: Session = Depends(get_db)):
    url = db.query(models.Urls).filter(models.Urls.shorturl == shorturl).first()

    if url is None:
        raise HTTPException(status_code = 404, detail = "URL no encontrada")
    
    db.delete(url)
    db.commit()
 
    return {"message": "URL eliminada con exito"}

@app.put("/urls/{shorturl}")
async def update_shorturl(shorturl: str, data: ShortUrlUpdate, db: Session = Depends(get_db)):
    db_url = db.query(models.Urls).filter(models.Urls.shorturl == shorturl).first()

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL no encontrada")
    
    db_url.shorturl = data.shorturl
    db.commit()
    db.refresh(db_url)

    return db_url
