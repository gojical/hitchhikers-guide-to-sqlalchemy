from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String, func, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

hc_mapper = Table(
    'hc_mapper',
    Base.metadata,
    Column('human_id', ForeignKey('humans.id')),
    Column('cat_id', ForeignKey('cats.id'))
)

class Human(Base):
    __tablename__ = "humans"
    id = Column(Integer, Sequence('human_seq'), primary_key=True)
    name = Column(String)
    # setting lazy=False for a cleaner output
    # this will load all of the child objects when the parent
    # is queried
    cats = relationship('Cat', secondary="hc_mapper", lazy=False)

class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, Sequence('cat_seq'), primary_key=True)
    name = Column(String)


# create a sqlite database in memory and show me the raw sql queries(echo=True)
engine = create_engine('sqlite:///:memory:')

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

# create a human object and populate it with data
libre = Human()
libre.name = "LibreLad"

cat1 = Cat()
cat1.name = "Scratches"

# relate cat1 to libre
libre.cats.append(cat1)

# add the object to the session
session.add(libre)

# commit the session to the DB
session.commit()


# lets see what the mapper table looks like
mapper_table = session.query(hc_mapper).all()
print "No. of records in mapper: %s" % len(mapper_table)
for field in mapper_table:
    print "human_id: %s | cat_id: %s" % (field.human_id, field.cat_id)

# get human from db
human_obj = session.query(Human).filter(Human.name == "LibreLad").first()

# remove cat1
human_obj.cats.remove(cat1)

session.add(human_obj)

# lets see what the mapper table looks like
mapper_table = session.query(hc_mapper).all()
print "No. of records in mapper: %s" % len(mapper_table)
for field in mapper_table:
    print "human_id: %s | cat_id: %s" % (field.human_id, field.cat_id)

# close the session
session.close()
