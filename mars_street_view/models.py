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

from sqlalchemy.orm.exc import (
    MultipleResultsFound,
    NoResultFound,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


class Photo(Base):
    def __init__(self, id=None, camera=None, rover=None, **kwargs):
        if rover:
            rover_name = rover['name']
            kwargs['rover_name'] = rover_name
        if camera:
            kwargs['camera_name'] = '_'.join((rover_name, camera['name']))
        else:
            raise KeyError('Photo must be initialized with a rover obj.')
        super(Photo, self).__init__(**kwargs)

    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    img_src = Column(String, nullable=False)
    sol = Column(Integer, nullable=False)
    earth_date = Column(String, nullable=False)
    rover_name = Column(String, ForeignKey('rovers.name'))
    camera_name = Column(String, ForeignKey('cameras.name'))
    rover = relationship('Rover', back_populates='photos')
    camera = relationship('Camera', back_populates='photos')

    def __json__(self, request):
        try:
            full_name = self.camera.full_name
        except AttributeError:
            full_name = ""          
        return {
        'id': self.id,
        'img_src': self.img_src,
        'sol': self.sol,
        'earth_date': self.earth_date,
        'rover_name': self.rover_name,
        'camera_name': self.camera_name,
        'camera_full_name': full_name
    }

    @classmethod
    def get_rov_sol(cls, rover, sol):
        return_dict = {}
        try:
            rover = DBSession.query(Rover).filter_by(name=rover).one()
        except NoResultFound:
            raise NoResultFound("Invalid rover name")

        except MultipleResultsFound:
            raise MultipleResultsFound("How did you even do that?")

        return_dict['rover'] = rover.name
        return_dict['sol'] = sol
        return_dict['photos_by_cam'] = {}

        # all_photos = DBSession.query(Photo).\
        #     filter(Photo.rover_name == rover.name, sol == sol).\
        #     order_by(Photo.id)

        for cam in rover.cameras:
            photos_this_cam = cam.photos.filter(Photo.sol == sol).all()
            return_dict['photos_by_cam'][cam.name] = photos_this_cam

        return return_dict


class Rover(Base):

    def __init__(self, cameras=None, **kwargs):
        super(Rover, self).__init__(**kwargs)

    __tablename__ = 'rovers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    landing_date = Column(String, nullable=False)
    max_date = Column(String, nullable=False)
    max_sol = Column(String, nullable=False)
    total_photos = Column(Integer, nullable=False)
    photos = relationship('Photo', back_populates='rover', lazy='dynamic')
    cameras = relationship('Camera', back_populates='rover', lazy='dynamic')


class Camera(Base):

    def __init__(self, name=None, **kwargs):
        if not kwargs.get('rover_name') or not name:
            raise KeyError('Camera must initialize with name and rover_name.')
        kwargs['name'] = '_'.join((kwargs['rover_name'], name))
        super(Camera, self).__init__(**kwargs)

    __tablename__ = 'cameras'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    rover_name = Column(String, ForeignKey('rovers.name'))
    full_name = Column(String, nullable=False)
    photos = relationship('Photo', back_populates='camera', lazy='dynamic')
    rover = relationship('Rover', back_populates='cameras')

# Index('my_index', MyModel.name, unique=True, mysql_length=255)
# TODO: write indexes for forthcoming tables.
