# create sqlalchemy con

from sqlalchemy import create_engine
import sqlahelper


from wam import settings  # pylint: disable=import-error


wam_config = settings.config['DATABASES']['OEP']

# ##########################################SQLAlchemy ENGINE#######################################
# db connection string for sqlalchemy-engine
DB_URL = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**wam_config)

engine = create_engine(DB_URL)
sqlahelper.add_engine(engine, 'oep_engine')
# ##################################################################################################
