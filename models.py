from django import forms

YEAR_CHOICES = [(y, '{}'.format(y)) for y in range(2002, 2010)]
MONTH_CHOICES = [(m, '{}'.format(m)) for m in range(1, 13)]

class SelectDateTime(forms.Form):
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    month = forms.ChoiceField(choices=MONTH_CHOICES)

    def __unicode__(self):
        return self.name
    idn = forms.HiddenInput()
