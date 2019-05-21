# serialize data for all models
from django.http import HttpResponse


import WAM_APP_FRED.oep_models as oep_modles
# from WAM_APP_FRED.db_sqla import *
from shapely.wkb import loads as loadswkb
from geojson import Feature, FeatureCollection, dumps
from geoalchemy2 import functions
import sqlahelper as sah
from datetime import datetime

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

class Serializer():
    """
    returns a query result containing a full record from OEP table model_draft.openfred_series
    as GEOJSON featureCollection. All related tables are joined and the values are included as
    property within the GEOJSON.

    :return: dict - geojson featureCollection
    """

    #ToDO: after testing done change to input pram
    Session = sah.get_session()
    session = Session()
    ##############################################

    def geometry_view(serlf):
        features = []

        for record in Serializer.session.query(oep_modles.classes['Series'],
                                               oep_modles.classes['Location'])\
                                                .join(oep_modles.classes['Location']).limit(100000):

            geometry = loadswkb(str(record.Series.location.point), True)
            feature = Feature(id=record.Series.id, geometry=geometry)
            features.append(feature)

        return HttpResponse(dumps(FeatureCollection(features)), content_type="application/json")



    def property_view(self):
        features = []

        for record in Serializer.session.query(oep_modles.classes['Series'],
                                    oep_modles.classes['Timespan'],
                                    oep_modles.classes['Variable']).join(oep_modles.classes['Timespan'])\
                                                                   .join(oep_modles.classes['Variable']).limit(1000):

            # Collection all Columns to be included from tables timespan and values
            # ToDo: maybe serialize the following on another session
            # record.Series.timespan.segments not included "list to long"
            # record.Series.values not included "list to long"
            # ToDo: How to handel the DateTimeObj so it is Json Serializeable
            # timespan_collection = {"Start": record.Series.timespan.start.strftime('%b %d %Y %I:%M%p'),
            #                        "Stop": record.Series.timespan.stop.strftime('%b %d %Y %I:%M%p'),
            #                        "Resolution": record.Series.timespan.resolution}

            netcdf = record.Series.variable.netcdf_attributes
            variables_collection = {"Name": record.Series.variable.name}
            variables_collection["NetCDF"] = netcdf


            propertys = {"SeriesID": record.Series.id, "values": record.Series.values, "height": record.Series.height}
            # propertys.update(timespan_collection)
            propertys.update(variables_collection)
            feature = Feature(id=record.Series.id, properties=propertys)
            features.append(feature)

        return HttpResponse(dumps(FeatureCollection(features)), content_type="application/json")

        # def get_single_weatherpoint(self, request):
        #     """
        #     Return the data for the closest weather-point for a given position
        #     as GeoJSON.
        #
        #     request: is the current mouse position passed from client
        #     :return:
        #     """
        #     if request.method is 'POST':
        #         position = request.POST.get('latlng')
        #
        #         for record in Serializer.session.query(oep_modles.classes['Series'],
        #                                                oep_modles.classes['Timespan'],
        #                                                oep_modles.classes['Variable'])\
        #                                                 .join(oep_modles.classes['Timespan']) \
        #                                                 .join(oep_modles.classes['Variable']).limit(1000):
        #
        #
        #             return HttpResponse(geojsondata, content_type="application/json")

