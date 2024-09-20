from pydantic import BaseModel
from typing import List, Optional
from geomatrix.ccmr.enums import LandTypeEnum, LandOwnershipType
from datetime import date
from uuid import UUID


class RequestCreateCadastreSchema(BaseModel):
    boundary_polygon: List[List[float]]  # List of coordinates [[lon, lat], [lon, lat], ...]
    land_type: LandTypeEnum
    ownership_type: LandOwnershipType
    area: Optional[float] = None
    elevation: Optional[float] = None
    slop: Optional[float] = None


class ResponseCreateCadastreSchema(BaseModel):
    cadastral_unique_id: str
    boundary_polygon: List[List[float]]
    land_type: LandTypeEnum
    ownership_type: LandOwnershipType
    location_coordinates: List[float]
    area: float
    elevation: float
    slop: float
    active_from: date
    created_by: UUID
