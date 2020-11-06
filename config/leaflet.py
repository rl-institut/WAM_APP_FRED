# Leaflet config: variable "LEAFLET_CONFIG" moved from settings.py to here
# since it conflicts with other apps using django-leaflet package.
# The leaflet config is now served via views.MapView() (uses settings override
# feature of django-leaflet)
# Related issue: https://github.com/rl-institut/WAM/issues/74

LEAFLET_CONFIG = {
    'TILES': [('OSM', 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
               {'attribution': '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
               }),
              ('OSM B&W', 'http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png',
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
