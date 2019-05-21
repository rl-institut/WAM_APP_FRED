# WAM_APP_FRED

This is a Django App witch based on the WAM Projekt.
----------------------
* **WAM: https://github.com/rl-institut/WAM**


Usage
----------------------
This App is based on Django. In Django we have one project with n applications. 
The base structure is provided within the project which is called WAM. A application
like WAM_APP_FRED extends the base structure of WAM and benefit from the provided 
structure/functionality.


Installation 
======================


####WAM
To run this application locally you need to complete the WAM setup first:  
* **WAM setup: https://wam.readthedocs.io/en/latest/getting_started.html**


####WAM_APP_FRED
The following steps have to be completed before running the local django server:

* clone this  repository into the WAM directory:
    ````
    -WAM <- folder you cloned the wam project
        -wam <- wam folder
        -wam_app <- wam_app folder
    ````

* While setting up the WAM you should have created a virtual environment(env) with all the 
packages the WAM needs. To set up the WAM_APP_FRED you need to extend this env with the 
packages found in wam_environment.yml 

* you need to add the app name to your environment variable "WAM_APPS = App1,App2,...."
You should have created the environment variable while setting up the WAM.

* in your config file you added while setting up the WAM, you need to provide a
valid OEP connection. The OEP is a external database. Because it is not known by django
we need to use a independent method to access the data.
!You will need to have access to the OEP! 
To handel the two different connections you will need to have 2 section with basically 
the same OEP connection credentials but a different Engine provided. Example can be found
[here](https://wam.readthedocs.io/en/latest/getting_started.html#configuration-file).

* Include this in your views.py
````
from django.shortcuts import render

def fred_map(request):
    return render(request, 'WAM_APP_FRED/fred_map.html')

````

* Include this in your urls.py
````
from django.urls import path
from . import views
app_name = 'WAM_APP_FRED'

urlpatterns = [
    path('', views.fred_map, name='index')
] 
````

LICENSE
-------