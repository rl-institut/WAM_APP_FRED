# WAM_APP_FRED

WAM_APP_FRED is a Django App which is part of the [WAM project](https://github.com/rl-institut/WAM).


## Overview

This App is based on Django. In Django we have one project with n applications. 
The base structure is provided within the project which is called WAM. A application
like WAM_APP_FRED extends the base structure of WAM and benefit from the provided 
structure/functionality.

## First steps

### Prerequisite

- clone WAM core project
```
git clone https://github.com/rl-institut/WAM.git
```
- complete the [setup of WAM](https://wam.readthedocs.io/en/latest/getting_started.html) core project

### Installation 

1. Clone the WAM_FRED_APP repository into the main directory of the WAM core project:
    ````
    - <WAM core>
        |
         - <WAM_APP_FRED>
        |
         - ...
    ````

2. Make sure you have added WAM_APP_FRED to the list of applications in the environment variable `WAM_APPS` 
which was created during the [setup of WAM](https://wam.readthedocs.io/en/latest/getting_started.html) core project.
You can check the value of `WAM_APPS` with the command
```
echo $WAM_APPS
```
which return value should contain at least `ẀAM_APP_FRED`.

3. The database used in this project is the [OEP](https://github.com/OpenEnergyPlatform) database which is a external database
 that is not managed by django. For this reason we use SQLAlchemy to manage the access to the data.
 This is set in the .config/config.cfg file of the WAM core project as follow :
 
 ```
 [DATABASES]
	[[DEFAULT]]
	    ENGINE = django.contrib.gis.db.backends.postgis
        USER = <username>
        PASSWORD = <password>
        HOST = oe2.iks.cs.ovgu.de
        PORT = 5432
        NAME = oedb
    [[OEP_LOCAL]]
        ENGINE = django.contrib.gis.db.backends.postgis
        NAME = oedb
        USER = <username>
        PASSWORD = <password>
        HOST = localhost
        PORT = 54321
    [[OEP]]
        ENGINE = postgresql+psycopg2
        USER = <username>
        PASSWORD = <password>
        HOST = oe2.iks.cs.ovgu.de
        PORT = 5432
        NAME = oedb
```
 
Enter your OEP credentials instead of <username> and <password>.


4. Run the local django server from the main directory of the WAM core project 

```
python manage.py runserver
````

## Usage

### Explore wind turbines informations and timeseries
 
### Explore weather data