from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DATABASE = "sqlite:///data.sqlite"

engine = create_engine(
    DATABASE,
    # TrueだとSQL文が出力される
    echo=False,
)

session = Session(autocommit=False, autoflush=True, bind=engine)

base = declarative_base()
# base.query = session.query_property()
