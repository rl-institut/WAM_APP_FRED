# app setting e.g. add default  map size
# flake8: noqa
# pylint: skip-file

LEAFLET_CONFIG = {
    # conf here

    'TILES': [('Streets', 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
               {'attribution': '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                'id': 'mapbox.streets',
                'maxZoom': 100,
                'minZoom': 9,
                }
               ),
              ('OSM B&W', 'http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png',
               {'attribution': '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                'minZoom': 9,
                }
               ),
              ('OSM', 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
               {'attribution': '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                'minZoom': 9,
                }),
              ('OpenTopoMap', 'http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
               {'attribution': 'Data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Display: &copy <a href="http://opentopomap.org">OpenTopoMap</a> <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                'minZoom': 9,
                })
              ],
    # Germany center (center = long/2 and lat/2)
    'DEFAULT_CENTER': (53.4554, 9.6211),
    'DEFAULT_ZOOM': 16,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 1000,
    'RESET_VIEW': False,
    'NO_GLOBALS': False,
}
