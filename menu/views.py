from django.views.generic import TemplateView


class MenuPageView(TemplateView):
    template_name = 'test_page.html'


class PendantPageView(TemplateView):
    template_name = 'test_page.html'
