from django.shortcuts import render
from .models import SelectDateTime
# Create your views here.


def fred_map(request):
    return render(request, 'WAM_APP_FRED/fred_map.html')


def webgui_test(request):
    start_date = SelectDateTime()
    end_date = SelectDateTime()
    return render(request, 'WAM_APP_FRED/test_map_layout.html', {"start_date": start_date,
                                                                 "end_date": end_date})
