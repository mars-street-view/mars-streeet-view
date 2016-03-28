from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


class Rover(Base):
    __tablename__ = 'rovers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    landing_date = Column(String, nullable=False)
    max_date = Column(String, nullable=False)
    max_sol = Column(String, nullable=False)
    total_photos = Column(Integer, nullable=False)
    photos = relationship('Photo', back_populates='rover')


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    img_src = Column(String, nullable=False)
    sol = Column(Integer, nullable=False)
    earth_date = Column(String, nullable=False)
    rover = relationship('Rover', back_populates='photos')
    rover_id = Column(Integer, ForeignKey('rovers.id'))

# Index('my_index', MyModel.name, unique=True, mysql_length=255)
# TODO: write indexes for forthcoming tables.
