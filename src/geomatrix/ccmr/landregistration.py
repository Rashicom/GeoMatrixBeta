from geomatrix.ccmr.schemas import RequestCreateCadastreSchema
import geopandas as gpd
from typing import List, Union
from geomatrix.ccmr.schemas import RequestCreateCadastreSchema
from pydantic import ValidationError

# Registration
class LandRegistrar:
    def __init__(self, data:Union[List[RequestCreateCadastreSchema],RequestCreateCadastreSchema], is_bulk = False):
        """
        defaultly this class expecting one land for registration(is_bulk=True)
        if you want to create bulk registration pass list of data and make is_bulk=False
        """
        # data type validaton check against is_bulk
        if is_bulk:
            if not isinstance(data, list):
                raise ValidationError("For bulk processing, 'data' must be a list of RequestCreateCadastreSchema")
            for item in data:
                if not isinstance(item, RequestCreateCadastreSchema):
                    raise ValidationError("Each item in the list must be an instance of RequestCreateCadastreSchema.")
        else:
            if not isinstance(data, RequestCreateCadastreSchema):
                raise ValidationError("data must be an instance of RequestCreateCadastreSchema.")
        self.land_list = data
        
    def validate(self):
        for land in self.land_list:
            # check length
            if len(land.boundary_polygon) < 3:
                raise ValueError(f"Boundary polygon for land with cadastral_unique_id {land.cadastral_unique_id} is not valid")
            # check if polygon is valid
            gdf = gpd.GeoDataFrame.from_features([{"geometry": gpd.Polygon(land.boundary_polygon), "properties": {}}])
            if not gdf.is_valid.all():
                raise ValueError(f"Boundary polygon for land with cadastral_unique_id {land.cadastral_unique_id} is not valid")

    def create_land(self):
        pass