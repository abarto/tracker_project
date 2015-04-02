from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'tracker_project/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['socket_io_url'] = 'http://{host}{port}/notifications'.format(
            host=self.request.META['SERVER_NAME'],
            port='' if self.request.META['SERVER_PORT'] == '80' else ':8002'
        )

        return context
home = HomeView.as_view()