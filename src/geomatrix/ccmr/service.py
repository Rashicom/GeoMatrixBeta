from geomatrix.ccmr.schemas import RequestCreateCadastreSchema
import geopandas as gpd

def validate_cadastre(cadastre_schema: RequestCreateCadastreSchema):
    """
        Pre Checks:
        - Form validation
        - Cadastre corditates validation
        - Cadastre overlaping validation (one cadastre must not overlap other cadastre)
    """
    # primary validation
    poligon_list = cadastre_schema.boundary_polygon

