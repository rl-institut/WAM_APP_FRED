# serialize data for all models
import datetime
from django.http import HttpResponse
from django.views import View
import sqlalchemy as sa
from sqlalchemy import and_
from sqlalchemy.orm import Bundle
import sqlahelper as sah
import geojson
from geojson import Point, MultiPolygon, Feature, FeatureCollection, dumps
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
from geoalchemy2.elements import WKTElement
from shapely.wkb import loads as loadswkb
from dateutil import parser


from .app_settings import LOCAL_TESTING, fred_config

if not LOCAL_TESTING:
    import WAM_APP_FRED.oep_models as oep_models
    from WAM_APP_FRED.oep_models import open_fred_classes

HOUR = '1:00:00'
HALF_HOUR = '0:30:00'
QUARTER = '0:15:00'
ZERO = '0:00:00'

TIME_STEPS = {
    HOUR: 60,
    HALF_HOUR: 30,
    QUARTER: 15,
    ZERO: 60,
}

# provide newest dataprocessing id
EGO_DP_VERSION = fred_config['WAM_APP_FRED']['EGO_DP_VERSION']


class Serializer(View):
    """
    Base Class for methods that return a the result of a SQL query in a non-proprietary file format.
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
        gj = geojson.load(g)

    def ger_boundaries_view(self):

        germany_boundaries = Serializer.gj

        return HttpResponse(dumps(germany_boundaries), content_type="application/json")

    def district_feedin_series_view(self):
        """
        This function will return a json/geojson with pre calculated data for a single or multiple
        district.
        The data will include a feedin time series for each district.
        :return:
        """
        pass


def ppr_view(request):
    """
    This function will return a geojson with all power-plants
    :return:
    """

    myfeatures = []

    if request.method == 'POST':
        region_id = str(request.POST.get('region_name'))
        # stores the current region boundary
        res_powerplant_tbl = oep_models.ego_dp_res_classes['ResPowerPlant']

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

        if LOCAL_TESTING is False:
            # Query the DB with the given wkbelement as input
            for wkb in wkbs:
                tbl_cols = Bundle('powerplant', res_powerplant_tbl.id, res_powerplant_tbl.geom,
                                  res_powerplant_tbl.generation_type, res_powerplant_tbl.scenario)

                oep_query = Serializer.session.query(tbl_cols) \
                    .filter(
                        and_(
                            tbl_cols.c.geom.ST_Within(wkb),
                            tbl_cols.c.scenario == 'Status Quo',
                            tbl_cols.c.generation_type == 'solar'
                        )
                    ).limit(1000)

                # ToDo: Insert dropdown selection in the filter options like 'solar'
                # ToDo: Change the geom column to rea_geom_new: mind there is another
                #  srid 3035 in this column
                for record in oep_query:

                    region_contains = loadswkb(str(record.powerplant.geom), True)

                    # feature_prop = Feature(id=record.powerplant.id, property='')
                    feature = Feature(
                        id=record.powerplant.id,
                        geometry=region_contains,
                        property=''
                    )
                    myfeatures.append(feature)
    elif request.method == 'GET':
        print(request.GET)

    return HttpResponse(dumps(FeatureCollection(myfeatures)), content_type="application/json")


def ppr_popup_view(request):
    """
        This function will return a geojson with all properties for a power-plant
        :return:
    """

    mypopup_content = []
    # pp = power plant
    if request.method == 'POST':
        # print(request.POST.get('pp_id'))
        pp_id = int(request.POST.get('pp_id'))
        # leaflet_id = int(request.POST.get('leaflet_id'))

        res_powerplant_tbl = oep_models.ego_dp_res_classes['ResPowerPlant']
        tbl_cols_property = Bundle(
            'powerplant_prop',
            res_powerplant_tbl.version,
            res_powerplant_tbl.id,
            res_powerplant_tbl.electrical_capacity,
            res_powerplant_tbl.generation_type,
            res_powerplant_tbl.generation_subtype,
            res_powerplant_tbl.city,
            res_powerplant_tbl.postcode,
            res_powerplant_tbl.voltage_level_var,
            res_powerplant_tbl.subst_id,
            res_powerplant_tbl.scenario
        )
        oep_query = Serializer.session.query(tbl_cols_property) \
            .filter(
            and_(
                tbl_cols_property.c.version == EGO_DP_VERSION,
                tbl_cols_property.c.id == pp_id
            )
        )

        for record in oep_query:
            region_property = dict(
                pp_id=record.powerplant_prop.id,
                # ToDo: How to convert from decimal
                electrical_capacity="",  # float(record.electrical_capacity),
                generation_type=record.powerplant_prop.generation_type,
                generation_subtype=record.powerplant_prop.generation_subtype,
                city=record.powerplant_prop.city,
                postcode=record.powerplant_prop.postcode,
                voltage_level=record.powerplant_prop.voltage_level_var,
                ego_subst_id=record.powerplant_prop.subst_id,
                scenario=record.powerplant_prop.scenario
            )
            feature_prop = Feature(id=record.powerplant_prop.id, property=region_property)
            mypopup_content = feature_prop
            # print(feature_prop)
    elif request.method == 'GET':
        print(request.GET)

    # print(mypopup_content)
    return HttpResponse(dumps(mypopup_content), content_type="application/json")


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
