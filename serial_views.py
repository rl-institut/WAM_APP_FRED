# serialize data for all models
from django.http import HttpResponse
from shapely.wkb import loads as loadswkb
from geojson import Feature, FeatureCollection, dumps
import sqlahelper as sah
import WAM_APP_FRED.oep_models as oep_modles
# from WAM_APP_FRED.db_sqla import *


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
    returns a query result containing a full record from OEP table as GEOJSON featureCollection.
    All related tables are joined and the values are included as property within the GEOJSON.

    :return: dict - geojson featureCollection
    """
    # pylint: disable=unnecessary-pass, no-self-use
    # ToDO: after testing done change to input pram
    Session = sah.get_session()
    session = Session()
    ##############################################

    def wseries_geometry_view(self):
        """
        returns a query result containing a full record from OEP table as GEOJSON
        featureCollection. Just the geometry is included.
        All related tables are joined and the values are included as property within the GEOJSON.

        :return:
        """

        features = []

        for record in Serializer.session.query(oep_modles.classes['Series'],
                                               oep_modles.classes['Location']) \
                .join(oep_modles.classes['Location']).limit(100000):

            geometry = loadswkb(str(record.Series.location.point), True)
            feature = Feature(id=record.Series.id, geometry=geometry)
            features.append(feature)

        return HttpResponse(dumps(FeatureCollection(features)), content_type="application/json")

    def wseries_property_view(self):
        """
        returns a query result containing a full record from OEP table as GEOJSON
        featureCollection. No geometry is included.
        All related tables are joined and the values are included as property within the GEOJSON.


        :return:
        """

        features = []

        for record in Serializer.session.query(
                oep_modles.classes['Series'],
                oep_modles.classes['Timespan'],
                oep_modles.classes['Variable']
        ).join(oep_modles.classes['Timespan']) \
                .join(oep_modles.classes['Variable']).limit(1000):

            # Collection all Columns to be included from tables timespan and values
            # ToDo: maybe serialize the following on another session
            # record.Series.timespan.segments not included "list to long"
            # record.Series.values not included "list to long"
            # ToDo: How to handel the DateTimeObj so it is Json Serializeable
            # timespan_collection = {
            #     "Start": record.Series.timespan.start.strftime('%b %d %Y %I:%M%p'),
            #     "Stop": record.Series.timespan.stop.strftime('%b %d %Y %I:%M%p'),
            #     "Resolution": record.Series.timespan.resolution
            # }

            netcdf = record.Series.variable.netcdf_attributes
            variables_collection = {"Name": record.Series.variable.name}
            variables_collection["NetCDF"] = netcdf

            propertys = {
                "SeriesID": record.Series.id,
                "values": record.Series.values,
                "height": record.Series.height
            }
            # propertys.update(timespan_collection)
            propertys.update(variables_collection)
            feature = Feature(id=record.Series.id, properties=propertys)
            features.append(feature)

        return HttpResponse(dumps(FeatureCollection(features)), content_type="application/json")

    def pp_list_geometry_view(self):
        """
        This function will return a geojson with all power-plants
        :return:
        """
        pass

    def kw_list_property_view(self):
        """
        This function will return a geojson with all properties' for each power-plant
        :return:
        """
        pass

    def district_feedin_series(self):
        """
        This function will return a json/geojson with pre calculated data for a single or multiple
        district.
        The data will include a feedin time series for each district.
        :return:
        """
        pass
