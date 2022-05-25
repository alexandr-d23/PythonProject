from django.urls import path, include

from url_shortener.views import Register, Home, ReducedUrls, Reduced

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),

    path('register/', Register.as_view(), name='register'),

    path('', include('django.contrib.auth.urls')),

    path('', Home.as_view(), name='home'),

    path('urls/', ReducedUrls.as_view(), name='urls'),

    path('<str:short>', Reduced.as_view(), name='redirect')
]
