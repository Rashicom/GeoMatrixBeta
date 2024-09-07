from geomatrix.enums import GeoMatrixEnum


class LandTypeEnum(GeoMatrixEnum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    ECOSENSITIVE = "ecosensitive"
    TRANSPORT = "transport"
    FOREST = "forest"
    WETLAND = "wetland"
    AGRICULTURAL = "agricultural"
    RIVER = "river"
    LAKE = "lake"


class LandFormedByEnum(GeoMatrixEnum):
    LAND_REGISTRATION = "land_registration"
    LAND_SPLIT = "land_split"
    LAND_MERGE = "land_merge"
    TYPE_CHANGE = "type_change"


class LandOwnershipType(GeoMatrixEnum):
    CENTRAL_GOV = "central_government"
    STATE_GOV = "state_government"
    LOCAL_SELF_GOV = "local_self_government"
    PRIVATE = "private"