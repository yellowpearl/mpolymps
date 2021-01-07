from django.shortcuts import render, HttpResponse
from django.views.generic import View

class AccountView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


    def post(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
