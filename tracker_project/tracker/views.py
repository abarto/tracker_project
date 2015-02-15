from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView


from .forms import IncidentForm
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
    form_class = IncidentForm

    def form_valid(self, form):
        form.instance.location = Point(
            float(form.cleaned_data['location_x']), float(form.cleaned_data['location_y'])
        )

        return super(IncidentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tracker:incident-list')
incident_create = IncidentCreateView.as_view()


class IncidentUpdateView(LoginRequiredMixin, UpdateView):
    model = Incident
    form_class = IncidentForm

    def get_initial(self):
        initial = super(IncidentUpdateView, self).get_initial()

        initial['location_x'] = self.get_object().location.x
        initial['location_y'] = self.get_object().location.y

        return initial

    def form_valid(self, form):
        form.instance.location = Point(
            float(form.cleaned_data['location_x']), float(form.cleaned_data['location_y'])
        )

        return super(IncidentUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tracker:incident-list')
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