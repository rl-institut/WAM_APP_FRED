# serialize data for all models
from django.http import HttpResponse
import geojson
from geojson import Point, MultiPolygon, Feature, FeatureCollection, dumps
from geoalchemy2 import functions as func
from geoalchemy2.shape import from_shape, to_shape
from shapely.wkb import loads as loadswkb
from shapely.wkt import loads, dumps as geomdumps
from shapely.geometry import MultiPolygon as sMP, Point, shape
import sqlahelper as sah
from sqlalchemy.orm import load_only, Bundle
from sqlalchemy import and_
import WAM_APP_FRED.oep_models as oep_models

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
#         geometry = loadswkb(str(record.point), True)
#         propertys = record.id
#         feature = Feature(id=record.id, geometry=geometry)
#
#         features.append(feature)
#
#     return dumps(FeatureCollection(features))


class Serializer():
    """
    Base Class for methods that retrun a Query result in a non-proprietary file format.
    Provides a the func. to get data (sql or api are main data sources)
    Mainly returns a query result containing a full record from OEP table as GEOJSON featureCollection.
    All related tables are joined and the values are included as property within the GEOJSON.
    :return: dict - geojson featureCollection
    """
    # pylint: disable=unnecessary-pass, no-self-use, no-self-argument
    # ToDO: after testing done change to input pram
    Session = sah.get_session()
    session = Session()
    ##############################################

    # list that stores all query results that are defined as feature object
    myfeatures = []
    with open('WAM_APP_FRED/static/WAM_APP_FRED/geodata/germany.geojson', encoding='UTF-8') as g:
    # ToDO: Remove after testing done
    # with open('F:\WAM\WAM_APP_FRED\static\WAM_APP_FRED\geodata\germany.geojson', encoding='UTF-8') as g:
    # with open(r'C:\Users\Jonas H\PycharmProjects\WAM\WAM_APP_FRED\static\WAM_APP_FRED\geodata\germany.geojson',
    #           encoding='UTF-8') as g:
        gj = geojson.load(g)

    def ger_boundaries_view(self):

        germany_boundaries = Serializer.gj

        return HttpResponse(dumps(germany_boundaries), content_type="application/json")

    def wseries_geometry_view(self):
        """
        returns a query result containing a full record from OEP table as GEOJSON
        featureCollection. Just the geometry is included.
        All related tables are joined and the values are included as property within the GEOJSON.
        :return:
        """

        # features = []
        #
        # with open('WAM_APP_FRED/static/WAM_APP_FRED/geodata/germany.geojson') as f:
        #     gj = geojson.load(f)
        #
        # print(len(gj['features']))
        # # for record in Serializer.session.query(
        # #         oep_models.classes['Series'],
        # #         oep_models.classes['Location']
        # # ).join(oep_models.classes['Location']).limit(10):
        # geometry = Point((10.01, 53.57))
        # # geometry = loadswkb(str(record.Series.location.point), True)
        # # feature = Feature(id=record.Series.id, geometry=geometry)
        # feature = Feature(id=101, geometry=geometry)
        # features.append(feature)

        # return HttpResponse(dumps(FeatureCollection(features)), content_type="application/json")
        # return HttpResponse(dumps(gj['features']), content_type="application/json")

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

    def ppr_view(self, request='Berlin'):
        """
        This function will return a geojson with all power-plants
        :return:
        """

        # if request.method == 'POST':
        #     print(request.POST)
        #     # lat = float(request.POST.get('lat'))
        #     # long = float(request.POST.get('long'))
        #     region_id = str()
        #     print(region_id)
        #
        #     if region_id in Serializer.gj['features']['properties']['name']:
        #         region_boundary = Serializer.gj['features']['geometry']['coordinates']
        #         geometry = MultiPolygon(region_boundary)
        #         # geometry = loadswkb(str(record.Series.location.point), True)
        #         # feature = Feature(id=record.Series.id, geometry=geometry)
        #         feature = Feature(id=102, geometry=geometry)
        #         self.features.append(feature)
        #
        # elif request.method == 'GET':
        #     print(request.GET)
        myfeatures = []
        region_id = str(request)
        # print(region_id)
        # stores the current region boundary
        wkbs = []
        for f in Serializer.gj['features']:
            if region_id in f['properties']['name']:
                region_boundary = f['geometry']['coordinates']
                boundary_geometry = MultiPolygon(region_boundary)
                # create shapely geometry from geojson feature
                _geom = shape(boundary_geometry)
                # convert shaply.geometry to wkbelement
                # query_geom = from_shape(_geom, srid=4326)

                # wkbs.append(_geom)
                # wkbs.append(from_shape(_geom, srid=3035))
                wkbs.append(from_shape(_geom, srid=4326))

                # feature = Feature(id=region_id, geometry=boundary_geometry)
                # feature = Feature(id=region_id, geometry=geometry)
                # self.features.append(feature)

        # Query the DB with the given wkbelement as input
        for wkb in wkbs:
            res_powerplant_tbl = oep_models.ego_dp_res_classes['ResPowerPlant']
            tbl_cols = Bundle('powerplant', res_powerplant_tbl.id, res_powerplant_tbl.electrical_capacity,
                              res_powerplant_tbl.generation_type, res_powerplant_tbl.generation_subtype,
                              res_powerplant_tbl.city, res_powerplant_tbl.postcode,
                              res_powerplant_tbl.voltage_level_var, res_powerplant_tbl.subst_id,
                              res_powerplant_tbl.geom, res_powerplant_tbl.scenario)

            # ToDo: Insert dropdown selection in the filter options like 'solar'
            # ToDo: Change the geom column to rea_geom_new mind there is another srid 3035 in this column
            for record in Serializer.session.query(tbl_cols)\
                    .filter(and_(tbl_cols.c.geom.ST_Within(wkb), tbl_cols.c.scenario == 'Status Quo',
                                 tbl_cols.c.generation_type == 'solar')).limit(1000):

                region_contains = loadswkb(str(record.powerplant.geom), True)
                feature_prop = ''
                feature = Feature(id=1, geometry=region_contains)
                myfeatures.append(feature)

                # print('WAIT')

        return HttpResponse(dumps(FeatureCollection(myfeatures)), content_type="application/json")

    # ToDO: this needed?
    def kw_list_property_view(self):
        """
        This function will return a geojson with all properties' for each power-plant
        :return:
        """
        pass

    def district_feedin_series_view(self):
        """
        This function will return a json/geojson with pre calculated data for a single or multiple
        district.
        The data will include a feedin time series for each district.
        :return:
        """
        pass

# ###########TESTING#####################
# sa = Serializer()
# POST_REGION = 'Bayern'
# sa.ppr_view(request=POST_REGION)
# print('WAIT')
# ########################################
