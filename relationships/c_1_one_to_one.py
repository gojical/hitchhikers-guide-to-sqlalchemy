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
    # using uselist=Flase to insure that the relationship is scalar
    # using back_populates to allow a bidirectional relatioship
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
    # Note that the back_populate args  match the opposite column names
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
                complaint="Bot stinks! Literally!")
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
