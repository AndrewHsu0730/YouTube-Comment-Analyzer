from sqlalchemy import Numeric, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from database import db

class User(db.Model):
    id = mapped_column(Integer, primary_key = True)
    username = mapped_column(String, unique = True, nullable = False)
    password = mapped_column(String, unique = True, nullable = False)

