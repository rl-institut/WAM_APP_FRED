from django.urls import path
from WAM_APP_FRED.serial_views import (
    Serializer,
    wseries_get_single_point,
    wseries_fetch_data_single_point
)
from . import views

app_name = 'WAM_APP_FRED'

urlpatterns = [
    # path('', views.fred_map, name='index')
    path('', views.webgui_test, name='index'),
    path('impressum', views.imprint, name='imprint'),
    path('privacy', views.privacy, name='privacy'),

    # just point geometrys as geojson featureCollection
    path('Locations.data/', Serializer.wseries_geometry_view, name='Locations.data'),
    path('MouseClick.data/', wseries_get_single_point, name='MouseClick.data'),
    path(
        'WeatherPointClick.data/',
        wseries_fetch_data_single_point,
        name='WeatherPointClick.data'
    ),
]
