from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from url_shortener.forms import UserCreationForm, UrlForm
from url_shortener.models import UrlWithShortcut


class Home(View):
    template_name = 'home.html'

    def get(self, request):
        context = {
            'form': UrlForm
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UrlForm(request.POST)
        print(form.url)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            print(form.cleaned_data)
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
