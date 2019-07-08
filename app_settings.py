import os
from sqlalchemy import create_engine
import sqlahelper
import oedialect  # noqa pylint: disable=unused-import
from configobj import ConfigObj

from wam import settings  # pylint: disable=import-error

# add local config file
fred_config = ConfigObj(os.path.join(settings.BASE_DIR, 'WAM_APP_FRED', 'config', 'fred_app.cfg'))

LOCAL_TESTING = settings.config['WAM'].as_bool('LOCAL_TESTING')
wam_config = settings.config['DATABASES']['OEP']
# wam_config = settings.config['DATABASES']['OEP_DIALECT']



# ##########################################SQLAlchemy ENGINE#######################################
if not LOCAL_TESTING:
    # db connection string for sqlalchemy-engine
    DB_URL = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**wam_config)
    # DB_URL = '{ENGINE}://{USER}:{TOKEN}@{HOST}'.format(**wam_config)
    engine = create_engine(DB_URL)
    sqlahelper.add_engine(engine, 'oep_engine')
# ##################################################################################################
