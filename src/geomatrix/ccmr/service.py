from geomatrix.ccmr.schemas import RequestCreateCadastreSchema
import geopandas as gpd
from geomatrix.ccmr.landregistration import LandRegistrar

def validate_cadastre(cadastre_schema: RequestCreateCadastreSchema):
    """
        Pre Checks:
        - Form validation
        - Cadastre corditates validation
        - Cadastre overlaping validation (one cadastre must not overlap other cadastre)
    """
    land_registrar = LandRegistrar(cadastre_schema, is_bulk=False)
    

