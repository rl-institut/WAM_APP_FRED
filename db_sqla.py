# contains functionality for all interactions with a connected database

from sqlalchemy import (
    BigInteger as BI,
    Column as C,
    DateTime as DT,
    Float,
    ForeignKey as FK,
    Integer as Int,
    Interval,
    JSON,
    MetaData,
    String as Str,
    Table,
    Text,
    UniqueConstraint as UC,)
from sqlalchemy.dialects.postgresql import ARRAY
import sqlahelper as sah

from geojson import Feature, FeatureCollection, dumps


import WAM_APP_FRED.oep_models

############################################SQLAlchemy setup####äääääääääääääää#########################################
SCHEMA = 'model_draft'
engine = sah.get_engine('oep_engine')
metadata = MetaData(schema=SCHEMA, bind=engine, reflect=True)


###################################################GeoJson-Serializer###################################################

session = sah.get_session()

def create_geojson():
    pass

def just_geom_geojson():
    pass

def just_property_geojson():
    pass

