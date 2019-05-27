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

* you need to add the app name to your environment variable "WAM_APPS = App1,App2,...."
You should have created the environment variable while setting up the WAM.

* in your config file which you created while setting up the WAM, you need to provide a
valid OEP connection. The OEP is a external database that is not managed by django. 
Because it is not known by django we need to use a independent method to access the data.
!You will need to have access to the OEP! 
To handel the two different databases (OEP, django internal) you will need to have 2 
sections in your config file. 
Example can be found [here](https://wam.readthedocs.io/en/latest/getting_started.html#configuration-file). 

fyi:
The OEP is accessed using SQLAlchemy. SQLA is using its own engine so there is a difference
how the engine value is named compared to the django engine. 
What are the differences between a Django engine:value and a SQLAlchemy engine:value?

````
In Django Config section:
ENGINE = django.contrib.gis.db.backends.postgis
````

````
In SQLAlchemy Config section:
ENGINE = postgresql+psycopg2
````

* To run the local django server just open up a console that can access the manage.py 
in the directory WAM and use the following command line input. If this fails 
you can try to debug it with the exception, or create a issue. 

````
python manage.py runserver
```` 

* If you are using linux it might be necessary to add "leaflet" to the installed_app list.
The list can be found here: 
````
path: WAM/wam/settings.py - INSTALLED_APPS[]
````
LICENSE
-------