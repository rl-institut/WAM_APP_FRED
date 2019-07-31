# Welcome Screen

Welcome

You can use this tool to get an example overview of the data used and generated in the OpenFRED project. OpenFRED stands for open Feed-in time series based on a Renewable Energy Database. The goal was to take weather and powerplant data and calculate the resulting energy feedin over time. It is possible to display and download a subset of the very large datasets. Full data can be accessed via the OpenEnergyPlatform.

Weather Data

The weather data were simulated at Helmholtz-Zentrum Geesthacht and cover Germany and its closer surroundings in a dense grid. Every point within the Grid includes 15 weather variables broken down to heights between 0 and 240 meters. Variables are calculated for several years with a resolution of 15 minutes. You can have a look at all weather data here: https://openenergy-platform.org/dataedit/view/model_draft/openfred_series

Power Plants

Power plants shown in the app are taken from the open_eGo project https://reiner-lemoine-institut.de/open_ego-open-electricity-grid-optimization/. Data can be accessed here: https://openenergy-platform.org/dataedit/view/supply/ego_dp_res_powerplant. At the time of these projects no comprehensive power plant dataset for Germany is available. Recently the German Federal Network Agency has published its internal data https://www.marktstammdatenregister.de/MaStR. However at the time of this writing the published data are still incomplete. A copy of the data can be accessed here: https://openenergy-platform.org/dataedit/view/supply/bnetza_eeg_anlagenstammdaten

Feedin Time Series

Feedin time series were caculated based on the extensive weather data and set of power plants. It is possible to use different dataset like MaStR with the developed feedinlib that is developed here: (link?). Currently shown data in this tool is for wind energy in the year 2016 and uses the open_eGo powerplant data.