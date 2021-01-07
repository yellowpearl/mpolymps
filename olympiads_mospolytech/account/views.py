from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .forms import UserRegistrationForm

class AccountView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


    def post(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')


class SignUp(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('http://127.0.0.1:8000/oll/')