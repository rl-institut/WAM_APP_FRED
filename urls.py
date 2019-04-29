from django.urls import path
from . import views
from WAM_APP_FRED.serial_views import serializer
app_name = 'WAM_APP_FRED'

urlpatterns = [
    # path('', views.fred_map, name='index')
    path('', views.webgui_test, name='index'),

    # 1 - Line
    # path('Lines.data/', serial_views.LinesData.as_view(), name='Lines.data'),

    path('Locations.data/', serializer(), name='Locations.data')
]
