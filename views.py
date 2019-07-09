from django.shortcuts import render
from .models import SelectDateTime
from WAM_APP_FRED.config.leaflet import LEAFLET_CONFIG
# Create your views here.


def fred_map(request):
    return render(request, 'WAM_APP_FRED/fred_map.html')


def imprint(request):
    return render(request, 'WAM_APP_FRED/imprint.html')


def privacy(request):
    return render(request, 'WAM_APP_FRED/privacy_policy.html')


def webgui_test(request):
    start_date = SelectDateTime()
    end_date = SelectDateTime()
    return render(
        request,
        'WAM_APP_FRED/test_map_layout.html',
        context={
            'leaflet_config': LEAFLET_CONFIG,
            'start_date': start_date,
            'end_date': end_date
        }
    )
