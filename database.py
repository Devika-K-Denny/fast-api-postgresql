from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine


engine=create_engine("postgresql://postgres:2205@localhost/item_db")

Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)
