from django.shortcuts import render
from WAM_APP_FRED.config.leaflet import LEAFLET_CONFIG
# Create your views here.


def fred_map(request):
    return render(request, 'WAM_APP_FRED/fred_map.html')


def imprint(request):
    return render(request, 'WAM_APP_FRED/imprint.html')


def privacy(request):
    return render(request, 'WAM_APP_FRED/privacy_policy.html')


def webgui_test(request):
    return render(
        request,
        'WAM_APP_FRED/test_map_layout.html',
        context={'leaflet_config': LEAFLET_CONFIG}
    )
