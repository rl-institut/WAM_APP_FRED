import sqlahelper as sah
import saio

saio.register_schema("model_draft", sah.get_engine('oep_engine'))
saio.register_schema("supply", sah.get_engine('oep_engine'))
from saio.model_draft import openfred_timeseries_wind_2016 as Timeseries
from saio.supply import ego_dp_res_powerplant as Powerplants
