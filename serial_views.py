# serialize data for all models

import WAM_APP_FRED.oep_models as oep_modles
# from WAM_APP_FRED.db_sqla import *
from shapely.wkb import loads
from geojson import Feature, FeatureCollection, dumps
from geoalchemy2 import functions
import sqlahelper as sah


def serializer():
    Session = sah.get_session()
    session = Session()

    features = []

    for record in session.query(oep_modles.classes['Location']).limit(100):
        geometry = loads(str(record.point), True)
        feature = Feature(id=record.id, geometry=geometry)
        features.append(feature)

    return dumps(FeatureCollection(features))


print(serializer())
print('WAIT')