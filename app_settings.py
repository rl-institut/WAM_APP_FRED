# create sqlalchemy con

import sqlahelper
from sqlalchemy import create_engine

from wam import settings


wam_config = settings.config['DATABASES']['OEP']

# ##########################################SQLAlchemy ENGINE#######################################
# db connection string for sqlalchemy-engine
DB_URL = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**wam_config)

engine = create_engine(DB_URL)
sqlahelper.add_engine(engine, 'oep_engine')
# ##################################################################################################
