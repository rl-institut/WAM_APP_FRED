from django.urls import path
from django.conf.urls import url
from . import views
from WAM_APP_FRED.serial_views import Serializer


from djgeojson.views import GeoJSONLayerView

from .models import WeatherStation

app_name = 'WAM_APP_FRED'

urlpatterns = [
    # path('', views.fred_map, name='index')
    path('', views.webgui_test, name='index'),

    # just point geometrys as geojson featureCollection
    path('Locations.data/', Serializer.wseries_geometry_view, name='Locations.data'),
    path('MouseClick.data/', Serializer.wseries_get_single_point, name='MouseClick.data'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=WeatherStation), name='data')
]
