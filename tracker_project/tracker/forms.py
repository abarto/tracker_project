from __future__ import absolute_import, unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.urlresolvers import reverse

from .models import AreaOfInterest, Incident


class IncidentForm(forms.ModelForm):
    location_geojson = forms.CharField(required=True, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        if kwargs.get('instance', None) is not None:
            self.helper.form_action = reverse('tracker:incident-update', kwargs={'pk': kwargs['instance'].pk})
        else:
            self.helper.form_action = reverse('tracker:incident-create')

        self.helper.render_hidden_fields = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Save', css_class='pull-right'))

    class Meta:
        model = Incident
        exclude = ('location',)


class AreaOfInterestForm(forms.ModelForm):
    polygon_geojson = forms.CharField(required=True, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(AreaOfInterestForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        if kwargs.get('instance', None) is not None:
            self.helper.form_action = reverse('tracker:area-of-interest-update', kwargs={'pk': kwargs['instance'].pk})
        else:
            self.helper.form_action = reverse('tracker:area-of-interest-create')

        self.helper.render_hidden_fields = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Save', css_class='pull-right'))

    class Meta:
        model = AreaOfInterest
        exclude = ('polygon',)