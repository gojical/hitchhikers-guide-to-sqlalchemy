from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String, func, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class Human(Base):
    __tablename__ = "humans"
    id = Column(Integer, Sequence('human_seq'), primary_key=True)
    name = Column(String)
    # setting lazy=False for a cleaner output
    # this will load all of the child objects when the parent
    # is queried

    # create a bidirectional relationship with the cat object,
    # when using backref you dont need to specify any
    # relationships on the child side
    # sqlalchemy will implicitly create a relationship
    # with secondary arguement
    cats = relationship('Cat', secondary=lambda: hc_mapper, backref="humans", lazy=False)

class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, Sequence('cat_seq'), primary_key=True)
    name = Column(String)

# create a sqlite database in memory and show me the raw sql queries(echo=True)
engine = create_engine('sqlite:///:memory:', echo=True)

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

# creating the mapper table last as a point for this example
hc_mapper = Table(
    'hc_mapper',
    Base.metadata,
    Column('human_id', ForeignKey('humans.id')),
    Column('cat_id', ForeignKey('cats.id'))
)

# this creates the table after we have run the create_all method.
hc_mapper.create(engine)

cat1 = Cat()
cat1.name = "Scratches"

# create a human object and populate it with data
libre = Human()
libre.name = "LibreLad"

# the FIRST need for mapping
libre.cats.append(cat1)

# add libre and cat1 to the session
session.add(libre)

# create other cat objects
cat2 = Cat()
cat2.name = "Patches"

cat3 = Cat()
cat3.name = "Wombat"

# relate the cats to the human
# since we added the cats to the human object
# the session will add the implicitly
libre.cats.extend([cat2, cat3])

# add libre to the session
session.add(libre)

# lets create a new user that will relate to some of the cats
# that libre relates to
libre_las = Human()
libre_las.name = "LibreLas"

# relate cats to libre_las
libre_las.cats.extend([cat1, cat3])

# add libre_las to the session
session.add(libre_las)

# commit the session
session.commit()

# lets get the relations of the cats from the user
def get_cats(human_obj):
    print "=================++++++++++++================="
    print "Begin query for parent and children"
    # this(query) is just to make sure that the object doesn't lazy load
    # there is no real merit to using this in
    # a real world scenario
    human_obj = session.query(Human).filter(Human.id == human_obj.id).first()
    print "----------------------------------------------"
    print "Human: %s's cats:" % human_obj.name
    for cat in human_obj.cats:
        print "cat_id: %s | cat_name: %s" % (cat.id, cat.name)
    print "=================++++++++++++=================\n"

get_cats(libre)
get_cats(libre_las)

# lets see what the mapper table looks like
mapper_table = session.query(hc_mapper).all()
for field in mapper_table:
    print "human_id: %s | cat_id: %s" % (field.human_id, field.cat_id)

# test back_populates bidirectional abilities
cat_obj = session.query(Cat).filter(Cat.name == "Wombat").first()

# show me the relationship between this cat and humans
for human in cat_obj.humans:
    print "%(cat)s knows %(human)s" % dict(cat=cat_obj.name, human=human.name)

# close the session
session.close()
