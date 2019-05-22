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
To handel the two different databases (OEP, django internal) you will need to have 2 sections. 
Example can be found [here](https://wam.readthedocs.io/en/latest/getting_started.html#configuration-file). 

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
provided by django (in dir WAM) and use the following command line input. If this fails 
you can try to debug this with the exception, or create a issue. 

````
python manage.py runserver
```` 

LICENSE
-------