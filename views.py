import csv
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from WAM_APP_FRED.config.leaflet import LEAFLET_CONFIG
from .models import CsvRow, CsvParam
from .forms import SelectDateTime, SelectVariable, SelectHeight, SelectTechnology

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


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def export_csv(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        height = request.POST.get('height')
        if height is None:
            height = 'none'
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(fname)
        CsvParam.objects.all().delete()
        CsvParam.objects.create(fname=fname, height=height)
    else:
        # get the filename and the height from a model
        fname = CsvParam.objects.all()[0].fname
        height = CsvParam.objects.all()[0].height

        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        to_write = [['Time', 'Value']]
        if height == 'none':
            subset = CsvRow.objects.all()
            for el in subset:
                to_write.append([el.time, el.val])
        else:
            subset = CsvRow.objects.filter(height__exact=height)
            for el in subset:
                to_write.append([el.time, el.val])

        response = StreamingHttpResponse(
            (writer.writerow(row) for row in to_write),
            content_type='text/csv'
        )
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(fname)

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
