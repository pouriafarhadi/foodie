from django.shortcuts import render
from django.views.generic import View


class Cprofile(View):
    def get(self, request):
        context = {}
        return render(request, "customer/customer-profile-page.html", context)
