"""accounts module URL Configuration

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

    path('actor/<str:nickname>/', views.actor_get_update),
    path('actor/', views.actor_create),
    path('creditcard/', views.creditcard_create),
    path('creditcard/<int:creditcard_id>/', views.creditcard_update_get),
]
