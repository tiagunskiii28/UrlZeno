from fastapi import FastAPI, HttpException, Depends
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

class urls(BaseModel):
    longurl: str
    shorturl: str
    alias: bool

