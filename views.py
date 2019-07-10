from django.shortcuts import render
from WAM_APP_FRED.config.leaflet import LEAFLET_CONFIG
from .forms import SelectDateTime, SelectVariable, SelectHeight
# Create your views here.


def fred_map(request):
    return render(request, 'WAM_APP_FRED/fred_map.html')


def imprint(request):
    return render(request, 'WAM_APP_FRED/imprint.html')


def privacy(request):
    return render(request, 'WAM_APP_FRED/privacy_policy.html')


def webgui_test(request):
    start_date = SelectDateTime(prefix='wd_timespan_start')
    end_date = SelectDateTime(prefix='wd_timespan_stop')
    variable = SelectVariable(prefix='wd')
    height = SelectHeight(prefix='wd')
    return render(
        request,
        'WAM_APP_FRED/test_map_layout.html',
        context={
            'leaflet_config': LEAFLET_CONFIG,
            'start_date': start_date,
            'end_date': end_date,
            'variable': variable,
            'height': height
        }
    )
