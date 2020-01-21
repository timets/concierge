from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now as django_now

class SimpleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.page_start_generate = django_now()
        request.fake_context = dict(data='test')

    def process_response(self, request, response):
        # just as sample
        return response
