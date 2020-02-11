import sqlahelper as sah
import saio

saio.register_schema("supply", sah.get_engine('oep_engine'))
from saio.supply import openfred_feedin_wind_2016 as Timeseries
from saio.supply import openfred_powerplants as Powerplants
