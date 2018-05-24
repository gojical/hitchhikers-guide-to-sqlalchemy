from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String, func, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class A(Base):
    __tablename__ = 'a'
    id = Column(Integer, Sequence('a_seq'), primary_key=True)
    name = Column(String(45))

class B(Base):
    __tablename__ = 'b'
    id = Column(Integer, primary_key=True)
    name = Column(String(45))

# create a sqlite database in memory and show me the raw sql queries(echo=True)
# dialect+driver://username:password@host:port/database
engine = create_engine('mysql://root@127.0.0.1:3306/tester1', echo=True)

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()


# commit objects to the database and close the session
# session.commit()
# session.close()
