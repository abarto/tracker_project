from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'tracker_project/home.html'
home = login_required(HomeView.as_view())