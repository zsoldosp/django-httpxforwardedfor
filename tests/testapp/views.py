from django.http import HttpResponse


def empty_page(request):
    return HttpResponse("")
