# Changelog
All notable changes to this project will be documented in this file.

The format is inpired from [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and the versiong aim to respect [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

Here is a template for new release sections

```
## [_._._] - 20XX-MM-DD

### Added
-
### Changed
-
### Removed
-
```

## [1.0.0] - 2019-09-19

### Added
- possibility to know which panel is selected
- feedinlib graph
- enabled local
- attribution to leaflet map
- possibility to download a CSV file
- filter option for weather data points (i.e. time span, variable id, height)
- geojson file with landkreis borders
- geojson file with rough counts of powerplants (to have an idea of how large it can be)
- powerplant specific icons

### Changed
- serializer view for data points, powerplants and feedinlib improved
- LOCAL_TESTING is set in `config/fred_app-cfg`
- the click on map will only trigger action for the selected panel
- improved README


## [0.0.1] - 2019-07-09

### Added
- CHANGELOG.md
- geojson serializer of the data from the oep API
- requirements.txt
- oep query for the openfred weather data
- license
- interactive click with the map to display weather data
- leaflet config file in config folder
- linting (.py files only)
- README

### Removed
- db_sqla.py file
- wam_environment.yml file

