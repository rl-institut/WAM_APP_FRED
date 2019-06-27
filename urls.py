from django.urls import path
from WAM_APP_FRED.serial_views import Serializer
from . import views

app_name = 'WAM_APP_FRED'

urlpatterns = [
    # path('', views.fred_map, name='index')
    path('', views.webgui_test, name='index'),

    # just point geometrys as geojson featureCollection
    path('Locations.data/', Serializer.wseries_geometry_view, name='Locations.data'),
    path('MouseClick.data/', Serializer.wseries_get_single_point, name='MouseClick.data'),
]
