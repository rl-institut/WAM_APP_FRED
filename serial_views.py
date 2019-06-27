# serialize data for all models
import datetime
from django.http import HttpResponse
import sqlalchemy as sa
import sqlahelper as sah
import geojson
from geojson import Point, Feature, FeatureCollection, dumps
from geoalchemy2.elements import WKTElement
from shapely.wkb import loads as loadswkb

# from .app_settings import LOCAL_TESTING
# if not LOCAL_TESTING:
#     import WAM_APP_FRED.oep_models as oep_models


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
    # pylint: disable=unnecessary-pass, no-self-use, no-self-argument
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

        with open('WAM_APP_FRED/static/WAM_APP_FRED/geodata/germany.geojson') as f:
            gj = geojson.load(f)

        print(len(gj['features']))
        # for record in Serializer.session.query(
        #         oep_models.classes['Series'],
        #         oep_models.classes['Location']
        # ).join(oep_models.classes['Location']).limit(10):
        geometry = Point((10.01, 53.57))
        # geometry = loadswkb(str(record.Series.location.point), True)
        # feature = Feature(id=record.Series.id, geometry=geometry)
        feature = Feature(id=101, geometry=geometry)
        features.append(feature)

        # return HttpResponse(dumps(FeatureCollection(features)), content_type="application/json")
        return HttpResponse(dumps(gj['features']), content_type="application/json")

    # def wseries_property_view(self):
    #     """
    #     returns a query result containing a full record from OEP table as GEOJSON
    #     featureCollection.
    #     No geometry is included.
    #     All related tables are joined and the values are included as property within the GEOJSON.
    #
    #
    #     :return:
    #     """
    #
    #     features = []
    #
    #     for record in Serializer.session.query(
    #             oep_models.classes['Series'],
    #             oep_models.classes['Timespan'],
    #             oep_models.classes['Variable']
    #     ).join(oep_models.classes['Timespan']).join(oep_models.classes['Variable']).limit(5):
    #
    #         # Collection all Columns to be included from tables timespan and values
    #         # ToDo: maybe serialize the following on another session
    #         # record.Series.timespan.segments not included "list to long"
    #         # record.Series.values not included "list to long"
    #         # ToDo: How to handel the DateTimeObj so it is Json Serializeable
    #         # timespan_collection = {
    #         "Start": record.Series.timespan.start.strftime('%b %d %Y %I:%M%p'),
    #         "Stop": record.Series.timespan.stop.strftime('%b %d %Y %I:%M%p'),
    #         #                        "Resolution": record.Series.timespan.resolution}
    #
    #         netcdf = record.Series.variable.netcdf_attributes
    #         variables_collection = {"Name": record.Series.variable.name}
    #         variables_collection["NetCDF"] = netcdf
    #
    #
    #         propertys = {
    #             "SeriesID": record.Series.id,
    #             "values": record.Series.values,
    #             "height": record.Series.height
    #         }
    #         # propertys.update(timespan_collection)
    #         propertys.update(variables_collection)
    #         feature = Feature(id=record.Series.id, properties=propertys)
    #         features.append(feature)
    #
    #     return HttpResponse(dumps(FeatureCollection(features)), content_type="application/json")

    def wseries_get_single_point(request):
        """
        Return the data for the closest weather-point for a given position
        as GeoJSON.
        The given position is provided as HTTP POST/GET method.

        request: is the current mouse position (@click) from client

        :return: GeoJSON feature as HTTP response
        """

        features = []
        if request.method == 'POST':
            print(request.POST)
            lat = float(request.POST.get('lat'))
            long = float(request.POST.get('long'))
            print(lat, long)
            geometry = Point((lat, long))
            # geometry = loadswkb(str(record.Series.location.point), True)
            # feature = Feature(id=record.Series.id, geometry=geometry)
            feature = Feature(id=102, geometry=geometry)
            features.append(feature)

            # for record in Serializer.session.query(
            #         oep_models.classes['Series'],
            #         oep_models.classes['Timespan'],
            #         oep_models.classes['Variable']
            # ).join(oep_models.classes['Timespan']
            # ).join(oep_models.classes['Variable']).limit(1000):
            #
            #     geom = ""
            #     propertys = ""
            #     feature = Feature(id= "", geometry=geom, property=propertys)
        elif request.method == 'GET':
            print(request.GET)

        return HttpResponse(dumps(FeatureCollection(features)), content_type="application/json")
        # return HttpResponse(feature, content_type="application/json")

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


def wseries_get_single_point(request):
    """
    Return the closest weather-point for a given position
    as GeoJSON.
    The given position is provided as HTTP POST/GET method.

    request: is the current mouse position (@click) from client

    :return: GeoJSON feature as HTTP response
    """

    features = []
    if request.method == 'POST':
        # get the latitude and longitude of the mouseClick event
        lon = float(request.POST.get('lon'))
        lat = float(request.POST.get('lat'))

        if not LOCAL_TESTING:
            clicked_p = WKTElement(f'POINT ({lon} {lat})', srid=4326)

            # Find the 5 nearest points from the mouse click in the oedb table
            # model_draft.openfred_locations, which has an 'id' and a 'point' column.
            # The point column is the geographical coordinates in a binary format
            oep_query = Serializer.session.query(open_fred_classes['Location']).order_by(
                open_fred_classes['Location'].point.distance_centroid(clicked_p)
            ).limit(5)
            nearest_points = []
            for record in oep_query:
                nearest_points.append(record.id)

            for record in oep_query:

                i = record.id
                coord = record.point
                pos = geojson.Feature(
                    geometry=loadswkb(str(coord), True),
                    properties=dict(
                        id=i
                    )
                )
                features.append(pos)

        else:
            pos = geojson.Feature(
                geometry=Point((lon, lat)),
                properties=dict(
                    id=101
                )
            )
            features.append(pos)
    elif request.method == 'GET':
        print(request.GET)

    return HttpResponse(dumps(FeatureCollection(features)), content_type="application/json")
