from __future__ import absolute_import, unicode_literals

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from tracker.models import Incident, AreaOfInterest


class HomeView(TemplateView):
    template_name = 'tracker_project/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['incidents'] = Incident.objects.filter(closed=False)
        context['areas_of_interest'] = AreaOfInterest.objects.all()

        return context
home = login_required(HomeView.as_view())