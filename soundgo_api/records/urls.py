"""records module URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('advertisement/', views.advertisement_create),
    path('advertisement/<int:advertisement_id>/', views.advertisement_update_get),
    path('audio/', views.audio_create),
    path('audio/<int:audio_id>/', views.audio_delete_get_update),
    path('audio/site/<int:site_id>/', views.audio_site_create),
    path('audio/site/categories/<int:site_id>/', views.audio_site_category_get),
    path('audio/listen/<int:audio_id>/', views.audio_listen),
    path('advertisement/listen/<int:advertisement_id>/', views.advertisement_listen),
    path('audio/like/<int:audio_id>/', views.like_create),
    path('audio/report/<int:audio_id>/', views.report_create)
]

