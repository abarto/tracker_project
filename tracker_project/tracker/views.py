from __future__ import absolute_import, unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import GEOSGeometry, Point
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from json import loads, dumps

from .forms import IncidentForm
from .models import Incident, AreaOfInterest


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class IncidentListOnSuccessMixin(object):
    def get_success_url(self):
        return reverse_lazy('tracker:incident-list')


class IncidentListView(LoginRequiredMixin, ListView):
    queryset = Incident.objects.all().order_by('-created')
incident_list = IncidentListView.as_view()


class IncidentDetailView(LoginRequiredMixin, DetailView):
    model = Incident
incident_detail = IncidentDetailView.as_view()


class IncidentCreateView(LoginRequiredMixin, IncidentListOnSuccessMixin, CreateView):
    model = Incident
    form_class = IncidentForm

    def get_initial(self):
        initial = super(IncidentCreateView, self).get_initial()

        initial['location_geojson'] = Point(0, 0).geojson

        return initial

    def form_valid(self, form):
        form.instance.location = GEOSGeometry(form.cleaned_data['location_geojson'])

        return super(IncidentCreateView, self).form_valid(form)
incident_create = IncidentCreateView.as_view()


class IncidentUpdateView(LoginRequiredMixin, IncidentListOnSuccessMixin, UpdateView):
    model = Incident
    form_class = IncidentForm

    def get_initial(self):
        initial = super(IncidentUpdateView, self).get_initial()

        initial['location_geojson'] = self.get_object().location.geojson

        return initial

    def form_valid(self, form):
        form.instance.location = GEOSGeometry(form.cleaned_data['location_geojson'])

        return super(IncidentUpdateView, self).form_valid(form)
incident_update = IncidentUpdateView.as_view()


class IncidentDeleteView(LoginRequiredMixin, IncidentListOnSuccessMixin, DeleteView):
    model = Incident
incident_delete = IncidentDeleteView.as_view()


class AreaOfInterestListView(LoginRequiredMixin, ListView):
    model = AreaOfInterest
area_of_interest_list = AreaOfInterestListView.as_view()


class AreaOfInterestDetailView(LoginRequiredMixin, DetailView):
    model = AreaOfInterest
area_of_interest_detail = AreaOfInterestDetailView.as_view()


class AreaOfInterestCreateView(LoginRequiredMixin, CreateView):
    model = AreaOfInterest
area_of_interest_create = AreaOfInterestCreateView.as_view()


class AreaOfInterestUpdateView(LoginRequiredMixin, UpdateView):
    model = AreaOfInterest
area_of_interest_update = AreaOfInterestUpdateView.as_view()


class AreaOfInterestDeleteView(LoginRequiredMixin, DeleteView):
    model = AreaOfInterest
area_of_interest_delete = AreaOfInterestDeleteView.as_view()