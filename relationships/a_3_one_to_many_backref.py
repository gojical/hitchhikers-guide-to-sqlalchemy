from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String, func, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class Person(Base):
    '''
    A simple person model with name and offence columns the id is the primary key.
    '''
    __tablename__ = 'person'
    id = Column(Integer, Sequence('person_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    # created a relationship with the Offence model and adds a virtual column person
    # where you can access the Person object from the Officences object
    offences = relationship('Offence', backref="person")

class Offence(Base):
    '''
    Offence that are logged against a person.
    '''
    __tablename__ = 'offences'
    id = Column(Integer, Sequence('offences_seq'), primary_key=True)
    description = Column(String(50), unique=True)
    person_id = Column(Integer, ForeignKey('persons.id'))

# create a sqlite database in memory, add kwarg echo=True to the
# raw SQL queries SQLA generates
engine = create_engine('sqlite:///:memory:')

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

# create a person and add them to the session
libre_lad = Person(name="L. Lad")
session.add(libre_lad)

# note that when you do a query, it commits all the current
# changes in the session to the database
libre_lad = session.query(Person).filter(Person.name == 'L. Lad').first()

# add an offence and supply it with a person_id
offence = Offence(description="Farting in public.", person_id=libre_lad.id)

# add an offence and supply it with a person_id
offence1 = Offence(description="Looking up skirts.", person_id=libre_lad.id)

# add an offence and supply it with a person_id
offence2 = Offence(description="Stealing from the homeless.", person_id=libre_lad.id)

# this offence has no person_id, however since we didn't make person_id
# NOT NULL(nullable=False) this is allowed...
offence3 = Offence(description="Public nudity.")

# add all offences to the database with add_all in session
session.add_all([offence, offence1, offence2, offence3])

# lets fetch the person object from the DB
person = session.query(Person).filter(Person.id == 1).first()

# a small test to see if we get the offences of the selected user.
print "%s's Offence:" % person.name
for offence in person.offences:
    print "offence: %s" % offence.description

e = session.query(Offence).filter(Offence.description == 'Stealing from the homeless.').first()
print e.person.name

# commit objects to the database and close the session
session.commit()
session.close()
