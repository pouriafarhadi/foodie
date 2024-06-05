from django.shortcuts import render
from django.views import View


def vprofile(request):
    return render(request, "vendor/vprofile-page.html")
