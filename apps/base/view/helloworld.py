# importing HttResponse from library
# Django imports
from django.http import HttpResponse


def home(request):
    # request is handled using HttpResponse object
    return HttpResponse("Hello there")
