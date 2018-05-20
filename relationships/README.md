#### *A hitchhiker's guide to SQLAlchemy <br> By LibreLad: Part-time hitchhiker* <br> **Relationship Basics**

> ⚠️**Warning: You *WILL* need a sense of humour to read this guide!** <br>
> A super simple guide on *One to Many, Many to One, One to One and Many to Many* Relationships <br>
> Most of the links in this guide link back to the [Official SQLAlchemy documentation](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html) <br>
> Please send ~~nudes~~ commits if you find any errors or if you can make an example clearer. <br>

---

##### Terminology:
* [`relationship`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html) : Creates the relationship between two classes `offence = relationship('Child')`
  * [`lazy`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html?highlight=lazy#sqlalchemy.orm.relationship.params.lazy) : if `True`, Only the parent object in question will load, once the object is accessed additional SELECT queries will be called to fetch the other objects data. More on this later 😏
  * [`backref`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref) : used to create *bidirectional* access to the parent model from the child model (MtO). backref as it sounds always refers to the name of the column that will be called from the child model to access the parent object eg: `backref='user'` this would be accessed as `child_obj.user` to retrieve the *Parent user object*.
  * [`back_populates`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates): works similar to backref, used to create an explicit relationship form child to parent. back_populates, as it sounds always refers to the *child object* relating to the *parent object*, eg: `back_populates='user'` this would be accessed the same a the eg. above.
  * [`uselist`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.uselist): is a boolean flag used to decide weather a relationship between the *Parent* and *Child* can be in list form or scalar(singular) form. This is used in *One to One* relationships.
* `Foreignkey` : A key that links two tables together. It's value is usually the parent `id`

---

##### Standard file layout for these examples :


> 🚑 The following examples were run in a *virtual environment* with `sqlalchemy` installed.

```python
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String, func, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

######################
#    models go here  #
######################

# create a sqlite database in memory and show me the raw sql queries(echo=True)
engine = create_engine('sqlite:///:memory:', echo=True)

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

###############################
#   session commands go here  #
###############################

# commit objects to the database and close the session
session.commit()
session.close()
```

---

##### A. [One to Many](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#one-to-many) :

###### Definition:
A *Parent* object can have a (OtM) relationship with a *Child* object, however this relationship **is not bidirectional** in it's simplest form, the *Parent* object can access the data in the *Child* object with a defined `relationship`. The *child* object holds a `ForeignKey` that references the *parent's* objects key(`id`) in order to filter out which records to return.

> 🚑 You can make OtM relationships bidirectional, see [`back_populates`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/a_2_one_to_many_back_populates.py) and [`backref`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/a_3_one_to_many_backref.py) examples in the [relationships folder](https://github.com/librelad/SQLAlchemy-Guide/tree/master/relationships).

###### Example:

```python
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String, func, DateTime
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
    offences = relationship('Offence')
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

# session.add(obj) will add the object to the session
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

# commit objects to the database and close the session
session.commit()
session.close()
```

###### Notes:
`ForeignKey`'s link to a field (table.column) and are accessible from the child.<br>
`relationship`'s link to Models, they use the ForeginKey as the [mapper](https://en.wikipedia.org/wiki/Map_(mathematics)) between the two Models.

---

##### B. [Many to One](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#many-to-one) :

###### Definition:
Both the `ForeignKey` and the `relationship` are in the *parent* object to create a relationship with the *child* object. There is no object mapping (ForeginKey) in the child model. **Many** parent objects can link to **one** specific child object.  

> 🚑 You can make MtO relationships bidirectional, see [`back_populates`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/b_2_many_to_one_back_populates.py) and [`backref`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/b_3_many_to_one_backref.py) examples in the relationships folder.

###### Example:

```python
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String, func, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
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

# add object to session
session.add(foot_fetish)

# fetch object from session
session.query(Website).filter(Website.id == 1).first()

# create user object relating to foot_fetish object
user1 = User(name="Jeff", website_id=foot_fetish.id)
user2 = User(name="Jeruska", website_id=foot_fetish.id)
user3 = User(name="Bongani", website_id=foot_fetish.id)

# add users to the session
session.add_all([user1, user2, user3])

# lets test our many to one by looking for the site url for Jeff
user_query = session.query(User).filter(User.name == "Jeff").first()

# accessing the one website from the user object
print "%s has been visiting" % user_query.name
print user_query.website.url

# commit objects to the database and close the session
session.commit()
session.close()

```

###### Notes:
`ForeignKey` and `relationship` are both in the parent model, the child model has no knowledge of the relationship. You can relate **one** child to many **parents** because the parent is the holder of the ForeginKey. Basic rule, whichever model holds the ForeginKey is the "Many" part of the relationship in most cases.

---

##### C. [One to One](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#one-to-one) :

###### Definition:
A one to one relationship is a *bidirectional* relationship between the *Parent* and *Child* objects with a [scalar](https://en.wikipedia.org/w/index.php?title=Scalar_(mathematics)&action=edit&section=8) attribute on both sides, this means that there is a check in place to make sure the neither the *Child* nor the *Parent* object can have more than one *bidirectional* relationship with the same models. We achieve this new behaviour with the [`uselist`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.uselist) kwarg.

> 🚑 OtO relationships use back_populates and backref by default to achieve the OtO relationship.

###### Example:

```python
from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String, func, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class Humanoid(Base):
    __tablename__ = 'humanoids'
    id = Column(Integer, Sequence('humanoid_seq'), primary_key=True)
    name = Column(String, nullable=False)
    date_initiated = Column(DateTime, default=func.now())
    complaint = Column(String, nullable=False)
    # create a relationship with the child model BarCode
    # using uselist=False to insure that the relationship is scalar
    # using back_populates to allow a bidirectional relationship
    # using lazy=False, to load(query) the BarCode child with the Humanoid obj
    barcode = relationship('BarCode', uselist=False, back_populates="humanoid", lazy=False)

class BarCode(Base):
    __tablename__ = 'overlord_barcodes'
    id = Column(Integer, Sequence('overload_bc_seq'), primary_key=True)
    actual = Column(String, nullable=False, unique=True)
    encryption_type = Column(String)
    # create a ForeginKey to map the Parent(Humanoid) object to this Child obj
    # set nullable=False which means that a parent id is
    # required to create a BarCode obj
    humanoid_id = Column(ForeignKey('humanoids.id'), nullable=False)
    # create a relationship with the Parent model in order to access
    # the parent object from the child
    # Note that the back_populates args  match the opposite column names
    # This is how the relationship is formed
    humanoid = relationship('Humanoid', uselist=False, back_populates="barcode")

# create a sqlite database in memory and show me the raw sql queries(echo=True)
engine = create_engine('sqlite:///:memory:', echo=True)

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

# create a humanoid object
bot1 = Humanoid(name="HalTron4000",
                complaint="Bot keeps flipping of little children.")
session.add(bot1)

# session.commit() will update the previous objects
# in this case bot1 which will fill in all of the
# fields that the database is responsible for.
session.commit()

# create a barcode object an add the humanoid.id to the params
barcode1 = BarCode(actual="AJX9w8r79w87Tskdjflsdfl47593457#009",
                   encryption_type="SHA256",
                   humanoid_id=bot1.id)

# add and commit the barcode obj
session.add(barcode1)
session.commit()

# a simple function to process the bot objects
def bot_info(bot_obj):
    print "===============++++==============="
    if not isinstance(bot_obj, Humanoid):
        print "The provided object is not a bot :("
    else:
        print "Now analysing bot id: %s" % bot_obj.id
        print "Bot Name: %s" % bot_obj.name
        print "Bot barcode: %s" % bot_obj.barcode.actual
        print "Initial Date bot came online: %s" % bot_obj.date_initiated
        print "Is bot Encrypted: %s" % bool(len(bot_obj.barcode.encryption_type))
        print "Bot complaint: %s" % bot_obj.complaint
        print "Analysis is finished."
    print "===============++++===============\n"

# lets access some data from the bot:
boj = session.query(Humanoid).filter(Humanoid.complaint is not None).first()
bot_info(boj)

# safe test:
bot_info(barcode1)

# commit objects to the database and close the session
session.commit()
session.close()

```

###### Notes:
One to One relationships are interesting because they incorporate `back_populates` or `backref` to create a bidirectional relationship between the two objects. The setup is simple if you have gone over OtM and MtO 😄.

---

##### D. [Many to Many](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#many-to-many) :

###### Definition:
A Many to Many relationship allows *parent* objects to have multiple *children* objects as well as share *children* objects. We create a mapper [table](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table) to keep track of which *parents* are related to specific *children*, we also add the [`secondary`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) kwarg to the relationship definition to show the model where the mapper table is.

> 🚑 You can make MtM relationships bidirectional, see [`back_populates`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/d_2_many_to_many_back_populates.py) and [`backref`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/d_3_many_to_many_backref.py) examples in the [relationships folder](https://github.com/librelad/SQLAlchemy-Guide/tree/master/relationships).

###### Example:

```python
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
engine = create_engine('sqlite:///:memory:', echo=True)

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

cat2 = Cat()
cat2.name = "Patches"

cat3 = Cat()
cat3.name = "Wombat"

# relate the cats to the human
# since we added the cats to the human object
# the session will add the implicitly
libre.cats.extend([cat1, cat2, cat3])

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

# close the session
session.close()
```

###### Notes:
Instead of adding the `id` in both columns of mapper table, we used `parent.relationship.extend([child_obj, child_obj2])` to add *multiple children objects* to the *Parent* object. You can also use `parent.relationship.append(child_obj)` to add 1 object.

The `secondary` kwarg can also be a lambda like so `secondary=lambda: mapper_table_obj`, the argument only runs when a mapper is needed, so long as you provide a valid mapper_table object when it is needed. [See example here](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/d_4_many_to_many_secondary_lambda.py).

You can define a `secondary` arg as the Table object or the string name of the table.

See [delete example](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/d_5_many_to_many_delete.py) and [delete all example](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/d_6_many_to_many_delete_all.py). There is alot of info on deleting MtM records please see the [SQLA Documentation on the subject](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#deleting-rows-from-the-many-to-many-table).

------

##### E. [Many to Many with Association](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object) :

###### Definition:
A Many to Many relationship allows *parent* objects to have multiple *children* objects as well as share *children* objects. We create a mapper [table](http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table) to keep track of which *parents* are related to specific *children*, we also add the [`secondary`](http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary) kwarg to the relationship definition to show the model where the mapper table is.

> 🚑 You can make MtM relationships bidirectional, see [`back_populates`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/d_2_many_to_many_back_populates.py) and [`backref`](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/d_3_many_to_many_backref.py) examples in the [relationships folder](https://github.com/librelad/SQLAlchemy-Guide/tree/master/relationships).

###### Example:

```python
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
engine = create_engine('sqlite:///:memory:', echo=True)

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

cat2 = Cat()
cat2.name = "Patches"

cat3 = Cat()
cat3.name = "Wombat"

# relate the cats to the human
# since we added the cats to the human object
# the session will add the implicitly
libre.cats.extend([cat1, cat2, cat3])

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

# close the session
session.close()
```

###### Notes:
Instead of adding the `id` in both columns of mapper table, we used `parent.relationship.extend([child_obj, child_obj2])` to add *multiple children objects* to the *Parent* object. You can also use `parent.relationship.append(child_obj)` to add 1 object.

The `secondary` kwarg can also be a lambda like so `secondary=lambda: mapper_table_obj`, the argument only runs when a mapper is needed, so long as you provide a valid mapper_table object when it is needed. [See example here](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/d_4_many_to_many_secondary_lambda.py).

You can define a `secondary` arg as the Table object or the string name of the table.

See [delete example](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/d_5_many_to_many_delete.py) and [delete all example](https://github.com/librelad/SQLAlchemy-Guide/blob/master/relationships/d_6_many_to_many_delete_all.py). There is alot of info on deleting MtM records please see the [SQLA Documentation on the subject](http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#deleting-rows-from-the-many-to-many-table).

---

##### And you're done...

![Deadpools_awesomeness](https://media.giphy.com/media/l4JyV4nyvJj834IZW/giphy.gif)
