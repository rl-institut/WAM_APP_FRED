# WAM_APP_FRED

WAM_APP_FRED is a Django App which is part of the [WAM project](https://github.com/rl-institut/WAM).


## Overview

The aim of this app is to display the content of the Open Energy Database of the
[Open Energy Platform (OEP)]((https://openenergy-platform.org/)) in an interactive way.

## First steps

### Prerequisite

- First, clone WAM core project
```
git clone https://github.com/rl-institut/WAM.git
```
- Then, complete the [setup of WAM](https://wam.readthedocs.io/en/latest/getting_started.html) core project

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

3. The database used in this project is the [OEDB](https://github.com/OpenEnergyPlatform/oeplatform) database which is a external database
 that is not managed by django. For this reason we use SQLAlchemy to access the data.
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
 
Enter your [OEP]((https://openenergy-platform.org/)) credentials instead of <username> and <password>.


4. Run the local django server from the main directory of the WAM core project 

```
python manage.py runserver
````

## Usage

Choose which type of data you would like to explore

### Explore weather data

The weather data from OEDB are available at a spatial resolution of 6 x 6 km with a time step of 15min.

First choose which weather data you would like to enquiry in the menu on the left.

Then, click on the map and a popup with the closest weather data point information will appear on the map.


### Explore wind turbines informations and timeseries
 
TDB