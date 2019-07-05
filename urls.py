from django.urls import path
from WAM_APP_FRED.serial_views import (
    Serializer,
    wseries_get_single_point,
    wseries_fetch_data_single_point,
    ppr_popup_view
)
from . import views

app_name = 'WAM_APP_FRED'

urlpatterns = [
    # path('', views.fred_map, name='index')
    path('', views.webgui_test, name='index'),
    # just point geometrys as geojson featureCollection
    # path('Locations.data/', Serializer.wseries_geometry_view, name='Locations.data'),
    path('MouseClick.data/', wseries_get_single_point, name='MouseClick.data'),
    path(
        'WeatherPointClick.data/',
        wseries_fetch_data_single_point,
        name='WeatherPointClick.data'
    ),
    path('GerBoundary.data/', Serializer.ger_boundaries_view, name='GerBoundary.data'),
    
    path('PowerPlantRegister.data/', Serializer.ppr_view, name='PowerPlantRegister.data'),
    path('PowerPlantPopup.data/', ppr_popup_view, name='PowerPlantPopup.data')

]
