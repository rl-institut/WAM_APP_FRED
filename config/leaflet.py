# Leaflet config: variable "LEAFLET_CONFIG" moved from settings.py to here
# since it conflicts with other apps using django-leaflet package.
# The leaflet config is now served via views.MapView() (uses settings override
# feature of django-leaflet)
# Related issue: https://github.com/rl-institut/WAM/issues/74

LEAFLET_CONFIG = {
    'TILES': [('Streets', 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
               {'attribution': 'Tiles: &copy; <a href="https://www.mapbox.com/about/maps/">mapbox</a>, Data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                'id': 'mapbox.streets',
                }),
              ('OSM B&W', 'http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png',
               {'attribution': '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
               }),
              ('OSM', 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
               {'attribution': '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                }),
              ('OpenTopoMap', 'http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
               {'attribution': 'Data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, Display: &copy <a href="http://opentopomap.org">OpenTopoMap</a> <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
                })
              ],

    'DEFAULT_CENTER': (51.9481, 10.2651),
    'DEFAULT_ZOOM': 0,
    'MAX_ZOOM': 40,
    'MIN_ZOOM': 6,
    'RESET_VIEW': False,
    'NO_GLOBALS': False,
}
