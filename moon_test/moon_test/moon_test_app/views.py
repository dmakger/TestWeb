from django.shortcuts import render
from django.views import View
from .models import Test


class MainView(View):
    def get(self, request, *args, **kwargs):
        tests = Test.objects.all()
        return render( request, 'moon_test_app/home.html', context={
            'tests': tests
        })