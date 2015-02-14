from __future__ import absolute_import, unicode_literals

from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Incident, AreaOfInterest


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class IncidentListView(LoginRequiredMixin, ListView):
    queryset = Incident.objects.all().order_by('-created')
incident_list = IncidentListView.as_view()


class IncidentDetailView(LoginRequiredMixin, DetailView):
    model = Incident
incident_detail = IncidentDetailView.as_view()


class IncidentCreateView(LoginRequiredMixin, CreateView):
    model = Incident
incident_create = IncidentCreateView.as_view()


class IncidentUpdateView(LoginRequiredMixin, UpdateView):
    model = Incident
incident_update = IncidentUpdateView.as_view()


class IncidentDeleteView(LoginRequiredMixin, DeleteView):
    model = Incident
incident_delete = IncidentDeleteView.as_view()


class AreaOfInterestListView(LoginRequiredMixin, ListView):
    queryset = AreaOfInterest.objects.all().order_by('-created')
area_of_interest_list = AreaOfInterestListView.as_view()


class AreaOfInterestDetailView(LoginRequiredMixin, DetailView):
    model = AreaOfInterest
area_of_interest_detail = AreaOfInterestDetailView.as_view()


class AreaOfInterestCreateView(LoginRequiredMixin, CreateView):
    model = Incident
area_of_interest_create = AreaOfInterestCreateView.as_view()


class AreaOfInterestUpdateView(LoginRequiredMixin, UpdateView):
    model = Incident
area_of_interest_update = AreaOfInterestUpdateView.as_view()


class AreaOfInterestDeleteView(LoginRequiredMixin, DeleteView):
    model = Incident
area_of_interest_delete = AreaOfInterestDeleteView.as_view()