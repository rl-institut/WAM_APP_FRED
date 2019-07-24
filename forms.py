from django import forms

YEAR_CHOICES = [(y, '{}'.format(y)) for y in range(2002, 2010)]
MONTH_CHOICES = [(m, '{}'.format(m)) for m in range(1, 13)]
VARIABLE_CHOICES = [
    (1, 'air_temperature'),
    (2, 'wind_speed'),
    (3, 'subsurface_runoff_amount'),
    (4, 'water_evaporation_amount'),
    (5, 'air_temperature'),
    (6, 'surface_normalized_direct_downwelling_shortwave_flux_in_air'),
    (7, 'air_pressure'),
    (8, 'snow_amount'),
    (9, 'surface_air_pressure'),
    # (10, None),
    (11, 'surface_runoff_amount'),
    (12, 'precipitation_amount'),
    (13, 'wind_speed'),
    (14, 'surface_roughness_length'),
    (15, 'surface_direct_downwelling_shortwave_flux_in_air')
]

TECHNOLOGY_CHOICES = [
    ('Wind', 'wind'),
    ('PV', 'pv'),
]

HEIGHTS = [0.0, 10.0, 80.0, 100.0, 120.0, 140.0, 160.0, 200.0, 240.0]
HEIGHT_CHOICES = [(h, '{}'.format(h)) for h in HEIGHTS]


class SelectDateTime(forms.Form):
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    month = forms.ChoiceField(choices=MONTH_CHOICES)

    def __unicode__(self):
        return self.name
    idn = forms.HiddenInput()


class SelectVariable(forms.Form):
    variable = forms.ChoiceField(choices=VARIABLE_CHOICES)

    def __unicode__(self):
        return self.name
    idn = forms.HiddenInput()


class SelectTechnology(forms.Form):
    technology = forms.ChoiceField(choices=TECHNOLOGY_CHOICES)

    def __unicode__(self):
        return self.name
    idn = forms.HiddenInput()


class SelectHeight(forms.Form):
    height = forms.ChoiceField(choices=HEIGHT_CHOICES)

    def __unicode__(self):
        return self.name
    idn = forms.HiddenInput()
