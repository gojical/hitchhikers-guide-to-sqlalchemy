from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String, func, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class HumanCarAssociation(Base):
    '''
    HumanCarAssociation accesses the Car as Many to One
    '''
    __tablename__ = 'human_car_association'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, default=func.now())

    human_id = Column(Integer, ForeignKey('humans.id'))
    car_id = Column(Integer, ForeignKey('cars.id'))

    cars = relationship('Car')

class Human(Base):
    '''
    Human accesses the Association as a One to Many relationship
    '''
    __tablename__ = 'humans'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    carsAssoc = relationship('HumanCarAssociation')

class Car(Base):
    '''
    car needs no relationships, because of the Many to One relationships
    '''
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    model = Column(String)

# create a sqlite database in memory and show me the raw sql queries(echo=True)
engine = create_engine('sqlite:///:memory:')

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

person = Human()
person.name = 'Libre'

car = Car()
car.model = "VW"

car2 = Car()
car2.model = "Tesla"

person2 = Human()
person2.name = 'LibreLas'

session.add_all([car, person, car2, person2])
session.commit()

assoc = HumanCarAssociation(human_id=person.id, car_id=car.id)
assoc2 = HumanCarAssociation(human_id=person.id, car_id=car2.id)
assoc3 = HumanCarAssociation(human_id=person2.id, car_id=car2.id)

session.add_all([assoc, assoc2, assoc3])
session.commit()

# query all associations
assocs = session.query(HumanCarAssociation).all()
for asses in assocs:
    print"human %s : car %s" % (asses.human_id, asses.car_id)

# get all cars for person
for cars in person.carsAssoc:
    print cars.cars.model

# get all people that drive the VW
drivers = session.query(Car).outerjoin(Car.id).filter(HumanCarAssociation.car_id == 1)
print drivers

# commit objects to the database and close the session
session.commit()
session.close()
