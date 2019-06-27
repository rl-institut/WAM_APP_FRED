from django.urls import path
from django.conf.urls import url
from djgeojson.views import GeoJSONLayerView
from WAM_APP_FRED.serial_views import (
    Serializer,
    wseries_get_single_point,
    wseries_fetch_data_single_point
)
from . import views
from .models import WeatherStation


app_name = 'WAM_APP_FRED'

urlpatterns = [
    # path('', views.fred_map, name='index')
    path('', views.webgui_test, name='index'),

    # just point geometrys as geojson featureCollection
    path('Locations.data/', Serializer.wseries_geometry_view, name='Locations.data'),
    path('MouseClick.data/', wseries_get_single_point, name='MouseClick.data'),
    path('WeatherPointClick.data/', wseries_fetch_data_single_point, name='WeatherPointClick.data'),
]
