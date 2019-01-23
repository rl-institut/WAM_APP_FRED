from django.shortcuts import render

# Create your views here.

def fred_map(request):
    return render(request, 'WAM_APP_FRED/fred_map.html')