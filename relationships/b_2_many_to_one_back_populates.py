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
    # creates a relationship with the users model that can be accessed by
    # the website object
    users = relationship('User', back_populates='website')

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

# create users object relating to foot_fetish object
users1 = User(name="Jeff", website_id=foot_fetish.id)
users2 = User(name="Jeruska", website_id=foot_fetish.id)
users3 = User(name="Bongani", website_id=foot_fetish.id)

# add userss to the session
session.add_all([users1, users2, users3])

# lets test our many to one by looking for the site url for Jeff
users_query = session.query(User).filter(User.name == "Jeff").first()

# accessing the one website from the users object
print "%s has been visiting" % users_query.name
print users_query.website.url

# test bidirectional access
print "Users in foot_fetish object"
for user in foot_fetish.users:
    print user.name

# commit objects to the database and close the session
session.commit()
session.close()
