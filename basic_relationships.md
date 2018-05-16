#### *A jackasses guide to SQLAlchemy <br> By LibreLad: Part-time Jackass* <br> **Relationship Basics**
---

##### Standard file layout for these examples :

```python
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

#######################
#    models go here  #
######################

# create a sqlite database in memory and show me the sql queries(echo=True)
engine = create_engine('sqlite:///:memory:', echo=True)

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

################################
#   session commands go here  #
################################

session.commit()
session.close()
```
---

##### [One to Many](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#one-to-many) :

###### Definition:
A *Parent table* can have a (OtM) relationship with a *child table*, however this relationship **is not bidirectional**, the *parent* can access the data in the *child* table with a defined `relationship`. The child table holds a `ForeignKey` that references the parent's key in order to filter out which records to return.

###### Example:

```python
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class Person(Base):
    '''
    A simple person model with name and offences columns the id is the primary key.
    '''
    __tablename__ = 'person'
    id = Column(Integer, Sequence('person_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    offences = relationship('Offences', lazy=True)

class Offences(Base):
    '''
    Offence that are logged against a person.
    '''
    __tablename__ = 'offences'
    id = Column(Integer, Sequence('arrests_seq'), primary_key=True)
    description = Column(String(50), unique=True)
    person_id = Column(Integer, ForeignKey('person.id'))

# create a sqlite database in memory, removed echo for a cleaner output
engine = create_engine('sqlite:///:memory:')

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

# create a peson and add them to the session
libre_lad = Person(name="L. Lad")
session.add(libre_lad)

# get the person object back from the DB this will populate
# all of the fields that the database is in charge of eg. id
libre_lad = session.query(Person).filter(Person.name == 'L. Lad').first()

# add an offence and supply it with a person_id
offence = Offences(description="Farting in public.", person_id=libre_lad.id)
session.add(offence)

# add an offence and supply it with a person_id
offence = Offences(description="Looking up skirts.", person_id=libre_lad.id)
session.add(offence)

# add an offence and supply it with a person_id
offence = Offences(description="Stealing from the homeless.", person_id=libre_lad.id)
session.add(offence)

# this offence has no person_id, however since we didnt make person_id
# NOT NULL this is allowed...
offence = Offences(description="Public nudity.")
session.add(offence)

# lets fetch the person object from the DB
person = session.query(Person).filter(Person.id == 1).first()

# a small test to see if we get the offecnes of the selected user.
print "%s's Offences:" % person.name
for offence in person.offences:
    print "offence: %s" % offence.description

# commit and close the session
session.commit()
session.close()

```

###### Terminology:
* [`relationship`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html) : Creates the relationship between two classes `offences = relationship('Offences')`
  * [`lazy`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html?highlight=lazy#sqlalchemy.orm.relationship.params.lazy) : when `True`, when you fetch the parent object it will fetch all of the child references.
  * [`backref`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref) : used to create *bidirectional* access to the parent model from the child model (MtO).
  * [`back_populates`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates): works similar to backref, used to create an explicit relationship form child to parent.
* `Foreignkey` : A key that links two tables together

###### Notes:
`ForeignKey`'s link to a field (table.column). `relationship`'s link to Models

###### `back_populates` Example:

```python
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class Person(Base):
    '''
    A simple person model with name and offences columns the id is the primary key.
    '''
    __tablename__ = 'person'
    id = Column(Integer, Sequence('person_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    # creates a relationship between models, and created a virtual column to link parent to child
    offences = relationship('Offences', back_populates="person")

class Offences(Base):
    '''
    Offence that are logged against a person.
    '''
    __tablename__ = 'offences'
    id = Column(Integer, Sequence('arrests_seq'), primary_key=True)
    description = Column(String(50), unique=True)
    # accesses the patrnt model from the child
    # this gets added in order to have an MtO accesser column
    person_id = Column(Integer, ForeignKey('person.id'))
    # creates a replationship from child to parent, use backref it's way more understandable
    person = relationship('Person', back_populates='offences')

# create a sqlite database in memory and make the sql queries verbose
engine = create_engine('sqlite:///:memory:')

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

# create a peson and add them to the session
libre_lad = Person(name="L. Lad")
session.add(libre_lad)

# get the person object back from the DB this will populate
# all of the fields that the database is in charge of eg. id
libre_lad = session.query(Person).filter(Person.name == 'L. Lad').first()

# add an offence and supply it with a person_id
offence = Offences(description="Farting in public.", person_id=libre_lad.id)
session.add(offence)

# add an offence and supply it with a person_id
offence = Offences(description="Looking up skirts.", person_id=libre_lad.id)
session.add(offence)

# add an offence and supply it with a person_id
offence = Offences(description="Stealing from the homeless.", person_id=libre_lad.id)
session.add(offence)

# this offence has no person_id, however since we didnt make person_id
# NOT NULL this is allowed...
offence = Offences(description="Public nudity.")
session.add(offence)

# lets fetch the person object from the DB
person = session.query(Person).filter(Person.id == 1).first()

# a small test to see if we get the offecnes of the selected user.
print "%s's Offences:" % person.name
for offence in person.offences:
    print "offence: %s" % offence.description

e = session.query(Offences).filter(Offences.description == 'Stealing from the homeless.').first()
print e.person.name

# commit and close the session
session.commit()
session.close()
```
