from django.shortcuts import render
from WAM_APP_FRED.config.leaflet import LEAFLET_CONFIG
from .forms import SelectDateTime, SelectVariable, SelectHeight, SelectTechnology
# Create your views here.


def fred_map(request):
    return render(request, 'WAM_APP_FRED/fred_map.html')


def imprint(request):
    return render(request, 'WAM_APP_FRED/imprint.html')


def privacy(request):
    return render(request, 'WAM_APP_FRED/privacy_policy.html')


def webgui_test(request):
    wd_start_date = SelectDateTime(prefix='wd_timespan_start')
    wd_end_date = SelectDateTime(prefix='wd_timespan_stop')
    variable = SelectVariable(prefix='wd')
    height = SelectHeight(prefix='wd')
    fd_start_date = SelectDateTime(prefix='fd_timespan_start')
    fd_end_date = SelectDateTime(prefix='fd_timespan_end')
    fd_technology = SelectTechnology(prefix='fd')
    return render(
        request,
        'WAM_APP_FRED/test_map_layout.html',
        context={
            'leaflet_config': LEAFLET_CONFIG,
            'wd_start_date': wd_start_date,
            'wd_end_date': wd_end_date,
            'variable': variable,
            'height': height,
            'fd_start_date': fd_start_date,
            'fd_end_date': fd_end_date,
            'fd_technology': fd_technology,
        }
    )
