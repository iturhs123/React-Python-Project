from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL= "postgresql://postgres:zreddit%23%401357@localhost:5432/telusco"
engine = create_engine(DATABASE_URL) 

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()