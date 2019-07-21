# serialize data for all models
import datetime
from django.http import HttpResponse
from django.views import View
from sqlalchemy import and_
from sqlalchemy.orm import Bundle
import sqlahelper as sah
import geojson
from geojson import Point, Feature, FeatureCollection, dumps
from geoalchemy2.shape import from_shape
from geoalchemy2.elements import WKTElement
from shapely.geometry import shape
from shapely.wkb import loads as loadswkb
from dateutil import parser


from .app_settings import LOCAL_TESTING, fred_config

if not LOCAL_TESTING:
    import WAM_APP_FRED.oep_models as oep_models
    from WAM_APP_FRED.oep_models import open_fred_classes, open_fred_ts_classes

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
EGO_DP_SCENARIO = fred_config['WAM_APP_FRED']['SCENARIO']


class Serializer(View):
    """
    Base Class for methods that return a the result of a SQL query in a non-proprietary file format.
    Provides a the func. to get data (sql or api are main data sources)
    Mainly returns a query result containing a full record from OEP table as
    GEOJSON featureCollection.
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

    # load the regions
    with open(
            'WAM_APP_FRED/static/WAM_APP_FRED/geodata/germany_nuts_1.geojson',
            encoding='UTF-8'
    ) as g:
        ger_regions = geojson.load(g)

    regions_wkbs = {}
    regions_nuts = {}
    for f in ger_regions['features']:
        region_id = f['properties']['region']
        region_boundary = f['geometry']['coordinates']
        boundary_geometry = geojson.MultiPolygon(region_boundary)
        # create shapely geometry from geojson feature
        _geom = shape(boundary_geometry)
        # store this information in a dict
        regions_wkbs[region_id] = from_shape(_geom, srid=4326)
        regions_nuts[region_id] = f['properties']['nuts_1']

    # load the landkreis
    with open(
            'WAM_APP_FRED/static/WAM_APP_FRED/geodata/germany_nuts_3.geojson',
            encoding='UTF-8'
    ) as g:
        ger_landkreis = geojson.load(g)

    landkreis_wkbs = {}
    landkreis_names = {}
    regions_to_landkreis = {}

    for f in ger_landkreis['features']:
        lk_id = f['properties']['nuts']
        lk_boundary = f['geometry']['coordinates']
        boundary_geometry = geojson.MultiPolygon(lk_boundary)
        # create shapely geometry from geojson feature
        _geom = shape(boundary_geometry)
        # store this information in a dict
        landkreis_wkbs[lk_id] = from_shape(_geom, srid=4326)
        # store the region index in a list
        landkreis_index.append(lk_id)

    def nuts_1_for_region(self, ppr_region):

        nuts_1 = []
        # load the map ot the landkreis for each region
        with open(
                # 'WAM_APP_FRED/static/WAM_APP_FRED/geodata/landkreis_map_to_region.json',
                'WAM_APP_FRED/static/WAM_APP_FRED/geodata/germany_nuts_3.geojson',
                encoding='UTF-8'
        ) as g:
            gj_to_lk = json.load(g)

        for i, f in enumerate(gj_to_lk['features']):
            if ppr_region in f['properties']['region']:
                nuts_1_temp = f['properties']['nuts_1']
                if nuts_1_temp not in nuts_1:
                    nuts_1.append(nuts_1_temp)

        return nuts_1

    def ger_boundaries_view(self):

        germany_boundaries = Serializer.ger_regions

        return HttpResponse(dumps(germany_boundaries), content_type="application/json")

    def ger_landkreis_view(self):

        germany_landkreis = Serializer.ger_landkreis

        return HttpResponse(dumps(germany_landkreis), content_type="application/json")

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
        generation_type = str(request.POST.get('generation_type'))
        if LOCAL_TESTING is False:
            # stores the current region boundary
            res_powerplant_tbl = oep_models.ego_dp_res_classes['ResPowerPlant']

        ser = Serializer()
        landkreis_ids = ser.nuts_1_for_region(region_id)
        if LOCAL_TESTING is False:
            # define the table columns for query
            tbl_cols = Bundle(
                'powerplant',
                res_powerplant_tbl.id,
                res_powerplant_tbl.nuts,  # added
                res_powerplant_tbl.version,
                res_powerplant_tbl.generation_type,
                res_powerplant_tbl.generation_subtype,
                res_powerplant_tbl.scenario
            )
            # create query
            # ToDo: Is there a way to apply ST_Transform to Bundle
            oep_query = Serializer.session.query(
                res_powerplant_tbl.rea_geom_new,
                tbl_cols
            ) \
                .filter(
                    and_(
                        # tbl_cols.c.rea_geom_new.ST_Transform(4326).ST_Within(wkb),
                        tbl_cols.c.nuts.in_(landkreis_ids),  # added
                        tbl_cols.c.version == EGO_DP_VERSION,
                        tbl_cols.c.scenario == EGO_DP_SCENARIO,
                        tbl_cols.c.generation_type == generation_type
                    )
                ).limit(1000)
            for record in oep_query:
                # TODO
                # this might need to be translated to 4326!!!
                region_contains = loadswkb(str(record[0]), True)
                feature = Feature(
                    id=record.powerplant.id,
                    geometry=region_contains,
                    property=dict(
                        region_id=region_id,
                        generation_type=generation_type,
                        generation_subtype=record.powerplant.generation_subtype
                    )
                )
                myfeatures.append(feature)
        else:
            for lk_id in landkreis_ids:
                lk_wkb = Serializer.landkreis_wkbs[lk_id]
                landkreis_center = loadswkb(str(lk_wkb), True).centroid

                feature = Feature(
                    id=lk_id,
                    geometry=landkreis_center,
                    property=dict(
                        region_id=region_id,
                        generation_type=generation_type,
                        generation_subtype='',
                    )
                )
                myfeatures.append(feature)

    elif request.method == 'GET':
        print(request.GET)

    return HttpResponse(dumps(FeatureCollection(myfeatures)), content_type="application/json")


def feedin_view(request):
    """
        Returns a geojson point with feedin-information over time.
    """

    myfeatures = []

    if request.method == 'POST':
        landkreis_props = {k: request.POST.get(k) for k in ['id', 'gen', 'bez', 'nuts']}
        lk_id = landkreis_props['nuts']
        # select the shape of the region
        wkbs = [Serializer.landkreis_wkbs[lk_id]]
        # Query the DB with the given wkbelement as input
        for wkb in wkbs:

            lk_contains = loadswkb(str(wkb), True).centroid
            feature = Feature(
                landkreis_id=lk_id,
                geometry=lk_contains,
                properties=landkreis_props
            )
            myfeatures.append(feature)

    elif request.method == 'GET':
        print(request.GET)

    return HttpResponse(dumps(FeatureCollection(myfeatures)), content_type="application/json")


def district_feedin_series(request):
    """
    This function will return a json/geojson with pre calculated data for a single or multiple
    district.
    The data will include a feedin time series for each district.
    :return:
    """
    data = []
    if request.method == 'POST':
        landkreis_props = {k: request.POST.get(k) for k in ['id', 'gen', 'bez', 'nuts']}
        lk_id = landkreis_props['nuts']
        if LOCAL_TESTING is False:
            openfred_ts_tbl = open_fred_ts_classes['OpenFredTimesSeries']
            oep_query = Serializer.session.query(openfred_ts_tbl)

            timespan = []
            values = []
            nut = ''
            for record in oep_query:
                timespan.append(record.time)
                values.append(record.feedin)
                nut = record.nut

            data = dict(
                landkreis_id=lk_id,
                timespan=timespan,
                values=values,
                nut=nut,
                properties=landkreis_props
            )
        else:
            data = dict(
                landkreis_id=lk_id,
                timespan=[
                    '2003-06-30T23:00:00',
                    '2003-07-01T00:00:00',
                    '2003-07-01T00:00:00',
                    '2003-07-01T01:00:00',
                    '2003-07-01T01:00:00',
                    '2003-07-01T02:00:00'
                ],
                values=[1, 3, 9, 16, 25, 36],
                nut='Wind',
                properties=landkreis_props
            )

    elif request.method == 'GET':
        print(request.GET)

    return HttpResponse(dumps(data), content_type="application/json")


def ppr_popup_view(request):
    """
        This function will return a geojson with all properties for a power-plant
        :return:
    """

    mypopup_content = []
    if request.method == 'POST':
        pp_id = int(request.POST.get('pp_id'))

        if LOCAL_TESTING is False:
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
                        tbl_cols_property.c.scenario == EGO_DP_SCENARIO,
                        tbl_cols_property.c.id == pp_id
                    )
                )

            record = oep_query.first()
            region_property = dict(
                pp_id=record.powerplant_prop.id,
                electrical_capacity=record.powerplant_prop.electrical_capacity,
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
        else:
            region_property = dict(
                pp_id=101,
                electrical_capacity=1700,
                generation_type='wind',
                generation_subtype='',
                city='Berlin',
                postcode=10000,
                voltage_level=100,
                ego_subst_id=101,
                scenario='Test'
            )
            feature_prop = Feature(id=101, property=region_property)
            mypopup_content = feature_prop
    elif request.method == 'GET':
        print(request.GET)

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
        start_year = str(request.POST.get('start_year'))
        start_month = int(request.POST.get('start_month'))
        end_year = int(request.POST.get('end_year'))
        end_month = int(request.POST.get('end_month'))

        start_time = '{}-{:02d}-01T00:00:00'.format(start_year, start_month)
        end_time = '{}-{:02d}-01T00:00:00'.format(end_year, end_month)

        if not LOCAL_TESTING:

            oep_query = Serializer.session.query(
                open_fred_classes['Series'],
                open_fred_classes['Timespan'],
                open_fred_classes['Variable'],
                open_fred_classes['Location'],
            ) \
                .filter(
                    and_(
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
                start_d = record.Series.timespan.start

                if isinstance(start_d, str):
                    start_d = parser.parse(start_d)

                end_d = record.Series.timespan.stop

                if isinstance(end_d, str):
                    end_d = parser.parse(end_d)

                cur_date = start_d
                t_res = record.Series.timespan.resolution

                if t_res == datetime.timedelta(0):
                    t_res += datetime.timedelta(hours=1)

                if isinstance(t_res, str):
                    dt = datetime.timedelta(minutes=TIME_STEPS[t_res])
                else:
                    dt = t_res

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
                    heights=["10.0"],
                    data={
                        10.0: {
                            'x': ['2003-06-30T23:00:00',
                                  '2003-07-01T00:00:00',
                                  '2003-07-01T00:00:00',
                                  '2003-07-01T01:00:00',
                                  '2003-07-01T01:00:00',
                                  '2003-07-01T02:00:00'],
                            'y': [1, 3, 9, 16, 25, 36]
                        }
                    },
                    variable=variable_id,
                    leaflet_id=leaflet_id,
                )
            )
            features = pos

    elif request.method == 'GET':
        print(request.GET)

    return HttpResponse(dumps(features), content_type="application/json")
