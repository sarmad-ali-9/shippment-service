from flask_sqlalchemy import SQLAlchemy
from sqlalchemy       import Column, String, Integer, \
    DateTime, ForeignKey
from sqlalchemy.orm   import relationship

db = SQLAlchemy()

class Vessel(db.Model):
    __tablename__  = "vessel"
    __table_args__ = {'extend_existing': True}
    id             = Column("vessel_id",    Integer, primary_key=True, autoincrement=True)
    name           = Column("name",         String,  nullable=False)
    owner_id       = Column("owner_id",     String,  nullable=False)
    naccs_code     = Column("naccs_code",   String,  nullable=False,   unique=True)
    voyages        = relationship('Voyage', back_populates='vessel')

    def __init__(self, name, owner_d, naccs_code):
        self.name       = name
        self.owner_id   = owner_d
        self.naccs_code = naccs_code

    def get_all_vessels():
        vessels = Vessel.query.all()
        return vessels

    def filter_by_naccs_code(naccs_code):
        vessels = Vessel.query.filter_by(naccs_code=naccs_code).first()
        return vessels


class Voyage(db.Model):
    __tablename__     = "voyage"
    __table_args__    = {'extend_existing': True}
    id                = Column("voyage_id",         Integer,  primary_key=True, autoincrement=True)
    start_time        = Column("start_time",        DateTime, nullable=False)
    end_time          = Column("end_time",          DateTime, nullable=False)
    start_location    = Column("start_location",    String,   nullable=False)
    end_location      = Column("end_location",      String,   nullable=False)
    vessel_naccs_code = Column("vessel_naccs_code", String,   ForeignKey('vessel.naccs_code'), nullable=False)
    vessel            = relationship('Vessel',      back_populates='voyages')

    def __init__(self, start_time, end_time, start_location, end_location, vessel_naccs_code):
        self.start_time        = start_time
        self.end_time          = end_time
        self.start_location    = start_location
        self.end_location      = end_location
        self.vessel_naccs_code = vessel_naccs_code

    def get_all_voyages():
        voyages = Voyage.query.all()
        return voyages

    def filter_by_naccs_code(naccs_code):
        voyages = Voyage.query.filter_by(vessel_naccs_code=naccs_code).all()
        return voyages

    def filter_by_voyage_id(voyage_id):
        voyages = Voyage.query.filter_by(id=voyage_id).first()
        return voyages

    def get_start_time_for_voyage(voyage_id):
        voyage = Voyage.query.get(voyage_id)
        start_time = voyage.start_time
        return start_time

    def get_end_time_for_voyage(voyage_id):
        voyage = Voyage.query.get(voyage_id)
        end_time = voyage.end_time
        return end_time

    def to_dict(self):
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "start_location": self.start_location,
            "end_location": self.end_location,
            "vessel_naccs_code": self.vessel_naccs_code
        }
