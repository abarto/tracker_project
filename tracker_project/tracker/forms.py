from __future__ import absolute_import, unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.urlresolvers import reverse

from .models import AreaOfInterest, Incident


class ReportIncidentForm(forms.ModelForm):
    location_description = forms.CharField(
        label='Location',
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'readonly': True, 'rows': 3})
    )
    location_lat = forms.DecimalField(required=True, widget=forms.HiddenInput)
    location_lon = forms.DecimalField(required=True, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(ReportIncidentForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_action = reverse('tracker:report-incident')
        self.helper.render_hidden_fields = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.add_input(Submit('submit', 'Report', css_class='btn-lg btn-block'))

    class Meta:
        model = Incident
        fields = ('location_description', 'location_lat', 'location_lon', 'name', 'description', 'severity')
        widgets = {
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            )
        }


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
        self.helper.field_class = 'col-lg-10'
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
        self.helper.field_class = 'col-lg-10'
        self.helper.add_input(Submit('submit', 'Save', css_class='pull-right'))

    class Meta:
        model = AreaOfInterest
        exclude = ('polygon',)