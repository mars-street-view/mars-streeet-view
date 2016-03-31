"""Defines models for the whole project: Photo, Rover and Camera."""
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text
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
    """Test model."""

    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


class Photo(Base):
    """Each individual photo object from a NASA API query."""

    def __init__(self, camera=None, rover=None, **kwargs):
        """Initialize the Photo object, renaming some parameters."""
        try:
            rover_name = rover['name']
            kwargs['rover_name'] = rover_name
        except AttributeError:
            raise KeyError('Photo must be initialized with a rover obj.')
        except KeyError:
            raise KeyError('Given rover object does not have a name.')
        try:
            kwargs['camera_name'] = '_'.join((rover_name, camera['name']))
        except AttributeError:
            raise KeyError('Photo must be initialized with a camera obj.')
        except KeyError:
            raise KeyError('Given camera object does not have a name.')
        super(Photo, self).__init__(**kwargs)

    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    img_src = Column(String, nullable=False, unique=True, index=True)
    sol = Column(Integer, nullable=False)
    earth_date = Column(String, nullable=False)
    rover_name = Column(String, ForeignKey('rovers.name'))
    camera_name = Column(String, ForeignKey('cameras.name'))
    rover = relationship('Rover', back_populates='photos')
    camera = relationship('Camera', back_populates='photos')

    def __json__(self, request):
        """Return dict of attributes which will be made into a JSON object."""
        try:
            full_name = self.camera.full_name
        except AttributeError:
            full_name = ''
        try:
            short_name = self.camera.short_name
        except AttributeError:
            short_name = ''
        return {
            'id': self.id,
            'img_src': self.img_src,
            'sol': self.sol,
            'earth_date': self.earth_date,
            'rover_name': self.rover_name,
            'camera_name': self.camera_name,
            'camera_short_name': short_name,
            'camera_full_name': full_name
        }

    @classmethod
    def get_rov_sol(cls, rover, sol):
        """Return photo data for a given Rover and mission sol."""
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

        for cam in rover.cameras:
            photos_this_cam = cam.photos.filter(Photo.sol == sol)
            ordered_photos = order_photo_query(photos_this_cam)
            return_dict['photos_by_cam'][cam.name] = ordered_photos

        return return_dict


def order_photo_query(photo_query):
    """Return custom sorted the given photo query."""
    # TODO: order by url instead
    return photo_query.order_by(Photo.id).all()


class Rover(Base):
    """Class for the three Mars rovers."""

    def __init__(self, cameras=None, **kwargs):
        """Initialize rover from NASA API JSON data, stripping out cameras."""
        super(Rover, self).__init__(**kwargs)

    __tablename__ = 'rovers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    landing_date = Column(String, nullable=False)
    max_date = Column(String, nullable=False)
    max_sol = Column(String, nullable=False)
    total_photos = Column(Integer, nullable=False)
    photos = relationship('Photo', back_populates='rover', lazy='dynamic')
    cameras = relationship('Camera', back_populates='rover', lazy='dynamic')


class Camera(Base):
    """Table of each camera on each Rover."""

    def __init__(self, name=None, **kwargs):
        """Construct camera object, resetting name to be Rovername_CAMNAME."""
        if not kwargs.get('rover_name') or not name:
            raise KeyError('Camera must initialize with name and rover_name.')
        kwargs['name'] = '_'.join((kwargs['rover_name'], name))
        kwargs['short_name'] = name
        super(Camera, self).__init__(**kwargs)

    __tablename__ = 'cameras'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    short_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    rover_name = Column(String, ForeignKey('rovers.name'))
    photos = relationship('Photo', back_populates='camera', lazy='dynamic')
    rover = relationship('Rover', back_populates='cameras')
