from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from url_shortener.forms import UserCreationForm, UrlForm
from url_shortener.models import UrlWithShortcut, get_short_url


class Reduced(View):
    def get(self, request, short):
        # short_url = short
        print(short)
        short_url = UrlWithShortcut.objects.get(url_shortcut=short)
        print(short_url)
        short_url.usage_count += 1

        short_url.save()

        return HttpResponseRedirect(short_url.full_url)


class Home(View):
    template_name = 'home.html'

    def get(self, request):
        context = {
            'form': UrlForm
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UrlForm(request.POST)

        if form.is_valid():
            model = form.save(commit=False)
            model.url_shortcut = get_short_url()
            model.user = request.user
            model.full_url = form.cleaned_data.get('full_url')
            model.save()

            url_shortcut = request.build_absolute_uri('/') + model.url_shortcut
            full_url = model.full_url

            context = {
                'form': UrlForm,
                'url_shortcut': url_shortcut,
                'full_url': full_url
            }

            return render(request, self.template_name, context)
        context = {
            'errors': form.errors
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


class ReducedUrls(View):
    template_name = 'urls.html'

    def get(self, request):
        user = request.user
        print('user id: ')
        print(user.id)
        urls = UrlWithShortcut.objects.filter(user_id=user.id).order_by('-usage_count')
        context = {
            'urls': urls
        }
        return render(request, self.template_name, context)

    def post(self, request):
        url_id = request.POST.get("url_id", "")
        print(url_id)
        if UrlWithShortcut.objects.filter(id=url_id).exists():
            UrlWithShortcut.objects.filter(id=url_id).delete()

        print('ended')
        return redirect("/urls/")
