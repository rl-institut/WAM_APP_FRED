# serialize data for all models
from django.http import HttpResponse

import WAM_APP_FRED.oep_models as oep_modles
# from WAM_APP_FRED.db_sqla import *
from shapely.wkb import loads
from geojson import Feature, FeatureCollection, dumps
from geoalchemy2 import functions
import sqlahelper as sah


# def serializer():
#     """
#     returns the queryed table id, geom as GEOJSON featureCollection
#     serializer for table without relations
#     :return: dict - geojson featureCollection
#     """
#
#     #ToDO: after testing done change to input pram
#     Session = sah.get_session()
#     session = Session()
#     ##############################################
#
#     features = []
#
#     for record in session.query(oep_modles.classes['Location']).limit(100):
#         geometry = loads(str(record.point), True)
#         propertys = record.id
#         feature = Feature(id=record.id, geometry=geometry)
#
#         features.append(feature)
#
#     return dumps(FeatureCollection(features))

def serializer():
    """
    returns the query result containing id, geom from table as GEOJSON featureCollection
    :return: dict - geojson featureCollection
    """

    #ToDO: after testing done change to input pram
    Session = sah.get_session()
    session = Session()
    ##############################################

    features = []

    for record in session.query(oep_modles.classes['Series'],
                                oep_modles.classes['Timespan'],
                                oep_modles.classes['Location'],
                                oep_modles.classes['Variable']).join(oep_modles.classes['Timespan'])\
                                                               .join(oep_modles.classes['Location'])\
                                                               .join(oep_modles.classes['Variable']).limit(100):
        geometry = loads(str(record.Series.location.point), True)

        # propertys = record.id  # dict
        feature = Feature(id=record.Series.location_id, geometry=geometry)

        features.append(feature)

    return dumps(FeatureCollection(features))


class GeoView():
    """
    geo view object
    """

    def geojson_view(self):
        """
        :return: Geojson as http response for url
        """
        geojsondata = serializer()
        # return render(geojsondata, GeoView.template_name, context={'geo_json':geojsondata})
        return HttpResponse(geojsondata, content_type="application/json")

    def geo_filter(self):
        pass


serializer()