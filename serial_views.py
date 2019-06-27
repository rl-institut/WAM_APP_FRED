# serialize data for all models
import datetime
from django.http import HttpResponse
import sqlalchemy as sa
import sqlahelper as sah
import geojson
from geojson import Point, Feature, FeatureCollection, dumps
from geoalchemy2.elements import WKTElement
from shapely.wkb import loads as loadswkb
from dateutil import parser

from .app_settings import LOCAL_TESTING
if not LOCAL_TESTING:
    from WAM_APP_FRED.oep_models import open_fred_classes

HOUR = '1:00:00'
HALF_HOUR = '0:30:00'
QUARTER = '0:15:00'
ZERO = '0:00:00'

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
TIME_STEPS = {
    HOUR: 60,
    HALF_HOUR: 30,
    QUARTER: 15,
    ZERO: 60,
}


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


def wseries_fetch_data_single_point(request):
    """
    Return the data a given weather-point as GeoJSON.
    The given position is provided as HTTP POST/GET method.

    request: is the current mouse position (@click) from client

    :return: GeoJSON feature as HTTP response
    """

    features = []
    if request.method == 'POST':
        # get the latitude and longitude of the mouseClick event
        lat = float(request.POST.get('lat'))
        lon = float(request.POST.get('lon'))
        leaflet_id = int(request.POST.get('leaflet_id'))
        location_id = int(request.POST.get('location_id'))
        variable_id = int(request.POST.get('variable_id'))
        start_time = str(request.POST.get('start_time'))
        end_time = str(request.POST.get('end_time'))

        if not LOCAL_TESTING:

            oep_query = Serializer.session.query(
                open_fred_classes['Series'],
                open_fred_classes['Timespan'],
                open_fred_classes['Variable'],
                open_fred_classes['Location'],
            ) \
                .filter(
                    sa.and_(
                        open_fred_classes['Timespan'].start >= start_time,
                        open_fred_classes['Timespan'].start <= end_time,
                        open_fred_classes['Variable'].id == variable_id,
                        open_fred_classes['Location'].id == location_id,
                    )
                ) \
                .join(open_fred_classes['Timespan']) \
                .join(open_fred_classes['Variable']) \
                .join(open_fred_classes['Location'])

            formatted_data = {}
            timespan_ids = []
            heights = []
            variable_name = ''
            for record in oep_query:
                variable_name = record.Series.variable.standard_name
                timespan_id = record.Series.timespan_id
                height = record.Series.height

                if timespan_id not in timespan_ids:
                    # resets the height list for every new timespan_id
                    heights = []
                    timespan_ids.append(timespan_id)

                if height not in heights:
                    heights.append(height)
                    # resets the data values for next height index
                    values = []
                    timespans = []

                # initialize the data indexes by height
                if height not in formatted_data:
                    formatted_data[height] = dict(x=[], y=[])

                # construct the values and the timestamps associated
                # the timespan goes from start date (included) to end_date (not included)
                # in steps depending on the resolution. It is easier to rebuild it than to
                # parse it as it is inputed as intervals of datetime values
                temp_values = record.Series.values
                start_d = parser.parse(record.Series.timespan.start)
                end_d = parser.parse(record.Series.timespan.stop)
                cur_date = start_d
                t_res = record.Series.timespan.resolution
                dt = datetime.timedelta(minutes=TIME_STEPS[t_res])
                idx = 0
                while cur_date <= end_d - dt:
                    values.append(temp_values[idx])
                    timespans.append(datetime.datetime.isoformat(cur_date))
                    cur_date = cur_date + dt
                    idx = idx + 1
                formatted_data[height]['x'] = formatted_data[height]['x'] + timespans
                formatted_data[height]['y'] = formatted_data[height]['y'] + values

            pos = geojson.Feature(
                geometry=Point((lon, lat)),
                properties=dict(
                    id='find_something_unique',
                    heights=[str(h) for h in heights],
                    variable=variable_name,
                    data=formatted_data,
                    leaflet_id=leaflet_id,
                )
            )
            features = pos
        else:
            pos = geojson.Feature(
                geometry=Point((lon, lat)),
                properties=dict(
                    id=101,
                    heights=["18.4"],
                    data={
                        18.4: {
                            'x': ['2003-06-30T23:00:00',
                                  '2003-07-01T00:00:00',
                                  '2003-07-01T00:00:00',
                                  '2003-07-01T01:00:00',
                                  '2003-07-01T01:00:00',
                                  '2003-07-01T02:00:00'],
                            'y': [1, 3, 9, 16, 25, 36]
                        }
                    },
                    variable='test_var',
                    leaflet_id=leaflet_id,
                )
            )
            features = pos

    elif request.method == 'GET':
        print(request.GET)

    return HttpResponse(dumps(features), content_type="application/json")
