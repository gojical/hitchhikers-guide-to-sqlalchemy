from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class Person(Base):
    '''
    A simple person model with name and offences columns the id is the primary key.
    '''
    __tablename__ = 'persons'
    id = Column(Integer, Sequence('person_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    # creates a relationship between models and created a virtual column to
    # link parent to child (offence)
    offences = relationship('Offence', back_populates="person")

class Offence(Base):
    '''
    Offence that are logged against a person.
    '''
    __tablename__ = 'offences'
    id = Column(Integer, Sequence('arrests_seq'), primary_key=True)
    description = Column(String(50), unique=True)
    # accesses the patent model from the child
    # this gets added in order to have an MtO accesser column
    person_id = Column(Integer, ForeignKey('persons.id'))
    # creates a replationship from child to parent
    # use backref it's way more understandable
    person = relationship('Person', back_populates='offences')

# create a sqlite database in memory, add kwarg echo=True to the the
# raw SQL queries SQLA generates
engine = create_engine('sqlite:///:memory:')

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

# create a peson and add them to the session
libre_lad = Person(name="L. Lad")
session.add(libre_lad)

# note that when you do a query it commits the changes to the database
# before fetchinig the object
libre_lad = session.query(Person).filter(Person.name == 'L. Lad').first()

# add an offence and supply it with a person_id
offence = Offence(description="Farting in public.", person_id=libre_lad.id)
session.add(offence)

# add an offence and supply it with a person_id
offence = Offence(description="Looking up skirts.", person_id=libre_lad.id)
session.add(offence)

# add an offence and supply it with a person_id
offence = Offence(description="Stealing from the homeless.", person_id=libre_lad.id)
session.add(offence)

# this offence has no person_id, however since we didn't make person_id
# NOT NULL this is allowed...
offence = Offence(description="Public nudity.")
session.add(offence)

# lets fetch the person object from the DB
person = session.query(Person).filter(Person.id == 1).first()

# a small test to see if we get the offecnes of the selected user.
print "%s's Offence:" % person.name
for offence in person.offences:
    print "offence: %s" % offence.description

e = session.query(Offence).filter(Offence.description == 'Stealing from the homeless.').first()
print e.person.name

# commit object to the database and close the session
session.commit()
session.close()
