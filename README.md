# WAM_APP_FRED

The WAM_APP_FRED is developed as an open-source web-application to visualize data that was collected or created 
within the project open_FRED. All data sources which are used within this web-application are open-source. The goal is 
to create an easily accessible and platform-independent web-application that can be used via the 
internet (using a web-browser). The main functionality the web-application provides is to visualize data on a map 
or additionally as graph. The app provide options for the user to interact with the visualized data. The web-application 
also provides functionality to get the data in a non proprietary format (like .csv).
The source data is divided into 3 main categories :
: Weather-Data, powerplant asset register and feedin-time-series. Each of these 
categories basically have there own source data. The data is provided within the open-energy-platform. Further explanation 
is given in the section source data. 

To achieve these requirements we use proven and open-source technologies. We use Django as Web-Framework. The base structure 
for this app is the Web Applications&Maps (WAM) project. Django
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

3. The database used in this project is the [OEDB](https://github.com/OpenEnergyPlatform/oeplatform) database which is 
a external database that is not managed by Django. For this reason we use SQLAlchemy to access the data.
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


4. Run the local Django server from the main directory of the WAM core project 

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

### Explore feedin time series data

The feedin time series data needs to be uploaded to the OEDB. Once this is finished it will be possible to present 
the data as graph within the WAM_APP_FRED. 

### Get data as .CSV file

The displayed data can be downloaded as csv file.
The file contains all the weather data for a single point selected on the map. 

## Source database

### Introducing the Open-Energy-Database

The database which is used as main data-source for all of the categories is the open-energy-database (OEDB). 
The OEDB is a postgreSQL database that was developed within the [open_eGo project](https://reiner-lemoine-institut.de/open_ego-open-electricity-grid-optimization/). 

### Introducing the Open-Energy-Platform

The OEDB is managed within the openenergy-platform (OEP). The OEP is the presentation layer for the OEDB. The OEP 
provides the Open-Energy Dialect (OED) which is a RestFUL API. Using the OED one can query the OEDB. The OEP provides 
the open-energy-dialect (OED) which is the main RestFul-API to query the OEDB. The data must be provided as a 
non-proprietary format like json or GEOJSON. 

 - OED on [GitHub](https://github.com/OpenEnergyPlatform/oedialect). 

In order to use the OED, one have to provide user credential. The credentials are represented by USER-NAME 
and TOKEN. One can get these credentials by signing-up to the OEP. 

- OEP can be found [here](https://openenergy-platform.org/)

### Access data from OEP

TBD

## Source data 

The following is an overview of the data sources used within the WAM_APP_FRED and provides where to find 
and how to access them.

| Category 1.         |          |
| ------------- | -------- |
| Category_name | weather-data (open_FRED)|
| Description | available in OEDB |
| Schema.Tablename |  <ul><li>model_draft.openfred_series</li></ul>|
| Relation (As FK)| <ul><li>model_draft.openfred_flags</li><li>model_draft.openfred_locations</li><li>model_draft.openfred_timespan</li><li>model_draft.openfred_variables</li></ul> |

| Category 2| |
| --- | --- |
| Category_name | power-plant facility register (open_eGo) |
| Description | available in OEDB, conventional energy:conv; renewable energy:res; mview´s are created for 3 scenarios |
| Schema.Tablename | <ul><li>supply.ego_dp_res_powerplant</li></ul> |


| Category 3 | |
| --- | ---- |
| Category_name | feedin-time-series () |
| Description | Currently available as python based pandas data-frames; OEDB upload will be in progress soon |
| Schema.Tablename | soon |
| Relation (As FK) | soon |

??? = Not known at the moment
soon = Will be provided soon
