import csv
from django.shortcuts import render
from django.http import HttpResponse
from WAM_APP_FRED.config.leaflet import LEAFLET_CONFIG
from .models import CsvRow, CsvName
from .forms import SelectDateTime, SelectVariable, SelectHeight, SelectTechnology
# Create your views here.


AVAILABLE_HEIGHTS = {
    1: [10., 80., 100., 120., 140., 160., 200., 240.],
    2: [10., 80., 100., 120., 140., 160., 200., 240.],
    3: [0.],
    4: [0.],
    5: [2.],
    6: [0.],
    7: [10., 80., 100., 120., 140., 160., 200., 240.],
    8: [0.],
    9: [0.],
    10: [0.],
    11: [0.],
    12: [0.],
    13: [10.],
    14: [0.],
    15: [0.]
}


def fred_map(request):
    return render(request, 'WAM_APP_FRED/fred_map.html')


def imprint(request):
    return render(request, 'WAM_APP_FRED/imprint.html')


def privacy(request):
    return render(request, 'WAM_APP_FRED/privacy_policy.html')


def update_heights(request):
    variable_id = int(request.GET.get('variable_id'))
    heights = AVAILABLE_HEIGHTS[variable_id]
    return render(request, 'WAM_APP_FRED/height_dropdown_list_options.html', {'heights': heights})


def export_csv(request):
    if request.method == 'POST':
        data = {k[0]: request.POST.getlist(k) for k in ['x[]', 'y[]']}
        fname = request.POST.get('fname')
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
        CsvName.objects.create(fname=fname)
        for x, y in zip(data['x'], data['y']):
            CsvRow.objects.create(time=x, val=y)
    else:

        response = HttpResponse(content_type='text/csv')
        fname = CsvName.objects.all()[0].fname
        CsvName.objects.all().delete()
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(fname)
        writer = csv.writer(response)
        writer.writerow(['Time', 'Value'])
        for el in CsvRow.objects.all():
            writer.writerow([el.time, el.val])
        CsvRow.objects.all().delete()
    return response


def webgui_test(request):
    wd_start_date = SelectDateTime(prefix='wd_timespan_start')
    wd_end_date = SelectDateTime(prefix='wd_timespan_stop', initial={'month': 2})
    variable = SelectVariable(prefix='wd')
    height = SelectHeight(prefix='wd', initial={'height': 10.0})
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
