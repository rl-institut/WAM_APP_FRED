#create sqlalchemy con

import os
import sqlahelper
from sqlalchemy import create_engine
from configobj import ConfigObj

from wam import settings
# from . import oep_models

# add the package leaflet to the wam core project installed apps
settings.INSTALLED_APPS.append('leaflet')
LOCAL_TESTING = True
############################################SQLAlchemy ENGINE#####+#####################################################
wam_config = settings.config['DATABASES']['OEP']
if LOCAL_TESTING is False:
    # db connection string for sqlalchemy-engine
    DB_URL = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**wam_config)

    engine = create_engine(DB_URL)
    sqlahelper.add_engine(engine, 'oep_engine')
########################################################################################################################

