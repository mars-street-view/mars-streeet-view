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

    def __init__(self, cameras=None, **kwargs):
        super(Rover, self).__init__(**kwargs)

    __tablename__ = 'rovers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    landing_date = Column(String, nullable=False)
    max_date = Column(String, nullable=False)
    max_sol = Column(String, nullable=False)
    total_photos = Column(Integer, nullable=False)
    photos = relationship('Photo', back_populates='rover', lazy='dynamic')
    cameras = relationship('Camera', back_populates='rover', lazy='dynamic')


class Photo(Base):
    def __init__(self, camera=None, rover=None, **kwargs):
        if camera:
            kwargs['camera_id'] = camera['id']
        if rover:
            kwargs['rover_id'] = rover['id']
        super(Photo, self).__init__(**kwargs)

    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    img_src = Column(String, nullable=False)
    sol = Column(Integer, nullable=False)
    earth_date = Column(String, nullable=False)
    rover_id = Column(Integer, ForeignKey('rovers.id'))
    camera_id = Column(Integer, ForeignKey('cameras.id'))
    rover = relationship('Rover', back_populates='photos')
    camera = relationship('Camera', back_populates='photos')


class Camera(Base):
    __tablename__ = 'cameras'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rover_id = Column(Integer, ForeignKey('rovers.id'))
    full_name = Column(String, nullable=False)
    photos = relationship('Photo', back_populates='camera')
    rover = relationship('Rover', back_populates='cameras')

# Index('my_index', MyModel.name, unique=True, mysql_length=255)
# TODO: write indexes for forthcoming tables.
