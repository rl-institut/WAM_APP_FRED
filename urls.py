from django.urls import path
from WAM_APP_FRED.serial_views import (
    Serializer,
    wseries_get_single_point,
    wseries_fetch_data_single_point,
    ppr_view,
    ppr_popup_view,
    district_feedin_series,
)
from . import views

app_name = 'WAM_APP_FRED'

urlpatterns = [
    # path('', views.fred_map, name='index')
    path('', views.webgui_test, name='index'),
    path('impressum', views.imprint, name='imprint'),
    path('privacy', views.privacy, name='privacy'),
    # just point geometrys as geojson featureCollection
    path('MouseClick.data/', wseries_get_single_point, name='MouseClick.data'),
    path(
        'WeatherPointClick.data/',
        wseries_fetch_data_single_point,
        name='WeatherPointClick.data'
    ),
    path('GerBoundary.data/', Serializer.ger_boundaries_view, name='GerBoundary.data'),
    path('PowerPlantRegister.data/', ppr_view, name='PowerPlantRegister.data'),
    path('PowerPlantPopup.data/', ppr_popup_view, name='PowerPlantPopup.data'),
    path('Feedinlib.data/', district_feedin_series, name='Feedinlib.data')

]
