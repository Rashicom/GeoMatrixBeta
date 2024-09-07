from geomatrix.database.core import Base
from geomatrix.models import TimeStampMixin
from geomatrix.ccmr.enums import LandTypeEnum, LandFormedByEnum, LandOwnershipType

from sqlalchemy import Column, String, Integer, Enum, Float, Date, ForeignKey
import uuid
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

# ccrm table
class CadastralRepository(Base, TimeStampMixin):
    """
    This table contains all the cadastral data.
    for each land operations like registration, splitting, type chane, merge, a new land is created
    and the previous land is considered as a prent land, and newly borned land from the parent land considred as the child land
    the parent child relationship of land is stored in the CadastralRepositoryRegistery Table.
    """
    __tablename__ = 'cadastral_repository'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # land unique id for each cadastral
    cadastral_unique_id = Column(String, nullable=False, unique=True)

    # land info
    boundary_polygon = Column(Geometry('POLYGON',srid=4326), nullable=False)
    land_type = Column(Enum(LandTypeEnum), nullable=False)
    ownership_type = Column(Enum(LandOwnershipType), nullable=False)

    # autogenerated fields
    location_coordinates = Column(Geometry('POINT',srid=4326), nullable=False)
    area = Column(Integer,nullable=False)
    elevation = Column(Float,nullable=True)
    slop = Column(Float,nullable=True)

    # land active status, active_from = registration time
    # active_till = land selled date. existing land is None. else a date
    # this dates is verry crucial for geberating land time snamshorts
    active_from = Column(Date, nullable=False)
    active_till = Column(Date, nullable=True)

    # created_by
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    # relationships
    parent_land_set = relationship("CadastralRegistery",foreign_keys="CadastralRegistery.child_land_id", back_populates="child_land")
    child_land_set = relationship("CadastralRegistery",foreign_keys="CadastralRegistery.parent_land_id", back_populates="parent_land")
    



class CadastralRegistery(Base, TimeStampMixin):
    """
    All Land operations relations are stored here
    for land, parent child relations are there
    """
    __tablename__ = 'cadastral_registery'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    parent_land_id = Column(UUID(as_uuid=True), ForeignKey('cadastral_repository.id', ondelete='CASCADE'), nullable=False)
    child_land_id = Column(UUID(as_uuid=True), ForeignKey('cadastral_repository.id', ondelete='CASCADE'), nullable=False)
    formed_by = Column(Enum(LandFormedByEnum), nullable=False)

    # relationships"back_populates"
    parent_land = relationship("CadastralRepository", foreign_keys=[parent_land_id], back_populates="child_land_set")
    child_land = relationship("CadastralRepository", foreign_keys=[child_land_id], back_populates="parent_land_set")
    
    type_change_register = relationship("CadastralTypeChangeRegistery", foreign_keys="CadastralTypeChangeRegistery.registery_id", back_populates="registry")




class CadastralTypeChangeRegistery(Base, TimeStampMixin):
    """
    Land type change are tracked here by pointing to the perticular registery
    """
    __tablename__ = 'cadastral_typechange_registery'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    registery_id = Column(UUID(as_uuid=True), ForeignKey('cadastral_registery.id', ondelete='CASCADE'), nullable=False)
    type_from = Column(Enum(LandTypeEnum), nullable=False)
    type_to = Column(Enum(LandTypeEnum), nullable=False)

    registry = relationship("CadastralRegistery", foreign_keys=[registery_id], back_populates="type_change_register")
