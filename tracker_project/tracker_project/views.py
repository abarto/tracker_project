from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'tracker_project/home.html'
home = HomeView.as_view()