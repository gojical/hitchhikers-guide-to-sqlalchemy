#### *A jackasses guide to SQLAlchemy <br> By LibreLad: Part-time Jackass* <br> **Relationship Basics**

> ⚠️**Warning: You *WILL* need a sense of humour to read this guide!** <br>
> A super simple guide to *One to Many, Many to One, One to One and Many to Many* Relationships <br>
> Most of the links in this guide link back to the [Official SQLAlchemy documentation](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html) <br>
> Please send ~~nudes~~ commits if you find any errors or if you can make an example clearer. <br>

---

##### Terminology:
* [`relationship`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html) : Creates the relationship between two classes `offences = relationship('Child')`
  * [`lazy`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html?highlight=lazy#sqlalchemy.orm.relationship.params.lazy) : if `True`, when you query a parent object it will fetch all of the child objects related to the selected parent obj.
  * [`backref`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref) : used to create *bidirectional* access to the parent model from the child model (MtO). backref as it sounds always refers to the name of the column that can be called from the child model to access the parent object eg: `backref='parent_tablename'`.
  * [`back_populates`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates): works similar to backref, used to create an explicit relationship form child to parent. back_populates, as it sounds ALWAYS refers to the child object populating the parent objects, eg: `back_populates='child_tablename'`.
* `Foreignkey` : A key that links two tables together

---

##### Standard file layout for these examples :


> 🚑 The following examples were run in a *virtual environment* with `sqlalchemy` installed.

```python
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

######################
#    models go here  #
######################

# create a sqlite database in memory and show me the sql queries(echo=True)
engine = create_engine('sqlite:///:memory:', echo=True)

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

###############################
#   session commands go here  #
###############################

session.commit()
session.close()
```

---

##### A. [One to Many](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#one-to-many) :

###### Definition:
A *Parent table* can have a (OtM) relationship with a *child table*, however this relationship **is not bidirectional**, the *parent* can access the data in the *child* table with a defined `relationship`. The child table holds a `ForeignKey` that references the parent's key in order to filter out which records to return.

> 🚑 You can make OtM relationships bidirectional, see [`back_populates`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/a_2_one_to_many_back_populates.py) and [`backref`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/a_3_one_to_many_backref.py) examples in the relationships folder.

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
    offences = relationship('Offences')

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
# session.add(obj) will add the object to the session
# which will implicitly process the automated database fields eg. id
session.add(libre_lad)

# get the person object back from the session this will populate
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
# NOT NULL(nullable=False) this is allowed...
offence = Offences(description="Public nudity.")
session.add(offence)

# lets fetch the person object from the DB
person = session.query(Person).filter(Person.id == 1).first()

# a small test to see if we get the offecnes of the selected user.
print "%s's Offences:" % person.name
for offence in person.offences:
    print "offence: %s" % offence.description

# commit object to the database and close the session
session.commit()
session.close()
```

###### Notes:
`ForeignKey`'s link to a field (table.column). `relationship`'s link to Models.

---

##### B. [Many to One](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#many-to-one) :

###### Definition:
Both the `ForeignKey` and the `relationship` are in the parent model to create a relationship with the child model. There is no object mapping (ForeginKey) in the child model. **Many** parent objects can link to **one** specific child object.  

> 🚑 You can make MtO relationships bidirectional, see [`back_populates`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/b_2_many_to_one_back_populates.py) and [`backref`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/b_3_many_to_one_backref.py) examples in the relationships folder.

###### Example:

```python
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    website_id = Column(Integer, ForeignKey('website.id'))
    website = relationship('Website')

class Website(Base):
    __tablename__ = 'website'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)

# create a sqlite database in memory and show me the sql queries(echo=True)
engine = create_engine('sqlite:///:memory:')

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

# create a website object
foot_fetish = Website(url="https://ffetish.co/no_idea_where_this_leads")

# add object to sesssion
session.add(foot_fetish)

# fetch object from session
session.query(Website).filter(Website.id == 1).first()

# create person object relating to foot_fetish object
person1 = Person(name="Jeff", website_id=foot_fetish.id)
person2 = Person(name="Jeruska", website_id=foot_fetish.id)
person3 = Person(name="Bongani", website_id=foot_fetish.id)

# add persons to the session
session.add(person1)
session.add(person2)
session.add(person3)

# lets test our many to one by looking for the site url for Jeff
person_query = session.query(Person).filter(Person.name == "Jeff").first()

# accessing the one website from the person object
print "%s has been visiting" % person_query.name
print person_query.website.url

# commit object to the database and close the session
session.commit()
session.close()
```

###### Notes:
`ForeignKey` and `relationship` are both in the parent model, the child model has no knowledge of the relationship.

---
