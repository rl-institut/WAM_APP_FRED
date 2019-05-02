from django.urls import path
from . import views
from WAM_APP_FRED.serial_views import GeoView
app_name = 'WAM_APP_FRED'

urlpatterns = [
    # path('', views.fred_map, name='index')
    path('', views.webgui_test, name='index'),

    # just point geometrys as geojson featureCollection
    path('Locations.data/', GeoView.geojson_view, name='Locations.data')
]
