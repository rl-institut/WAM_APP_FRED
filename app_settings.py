#create sqlalchemy con

import os
import sqlahelper
from sqlalchemy import create_engine
from configobj import ConfigObj

from wam import settings
from . import oep_models


wam_config = settings.config['DATABASES']['OEP']

############################################SQLAlchemy ENGINE#####+#####################################################
DB_URL = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}'.format(**wam_config)
# DB_URL = '{}://{}:{}@{}:{}'.formt()

engine = create_engine(DB_URL)
sqlahelper.add_engine(engine)
########################################################################################################################
