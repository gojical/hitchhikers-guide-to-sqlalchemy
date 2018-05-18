from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class Person(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    website_id = Column(Integer, ForeignKey('website.id'))
    # creating a virtual column that will give the website object
    # access to attached user objects
    website = relationship('Website', backref='users')

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

# create user object relating to foot_fetish object
user1 = Person(name="Jeff", website_id=foot_fetish.id)
user2 = Person(name="Jeruska", website_id=foot_fetish.id)
user3 = Person(name="Bongani", website_id=foot_fetish.id)

# add users to the session
session.add(user1)
session.add(user2)
session.add(user3)

# lets test our many to one by looking for the site url for Jeff
user_query = session.query(Person).filter(Person.name == "Jeff").first()

# accessing the one website from the user object
print "%s has been visiting" % user_query.name
print user_query.website.url

# test bidirectional access
for people in foot_fetish.users:
    print people.name

# commit objects to the database and close the session
session.commit()
session.close()
