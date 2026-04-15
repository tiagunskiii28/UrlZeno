from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Urls(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    longurl = Column(String, index=True)
    shorturl = Column(String, index=True)
    alias = Column(String, index=True)