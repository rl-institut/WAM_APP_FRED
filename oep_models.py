# Add all open_FRED table models form source DB: OEP

from sqlalchemy import create_engine, MetaData, Table, Column, MetaData, ARRAY, BigInteger, Boolean, \
                        Column, Float, ForeignKey, Integer, JSON, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import sqlahelper as sah

from geoalchemy2.types import Geometry
from WAM_APP_FRED.cli.openFRED import mapped_classes, db_session


############################################SQLAlchemy setup####äääääääääääääää#########################################
SCHEMA = 'model_draft'
engine = sah.get_engine()
metadata = MetaData(schema=SCHEMA, bind=engine, reflect=True)

############################################TABLE DEFINITION############################################################

classes = mapped_classes(metadata)