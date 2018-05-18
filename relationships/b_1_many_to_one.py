from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String
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
