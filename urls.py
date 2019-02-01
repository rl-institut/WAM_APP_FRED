from django.urls import path
from . import views
app_name = 'WAM_APP_FRED'

urlpatterns = [
    path('', views.fred_map, name='index')

]
