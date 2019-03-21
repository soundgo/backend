"""soundgo_api URL Configuration

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

from django.contrib import admin
from django.urls import include
from rest_framework_simplejwt import views as jwt_views
from django.urls import path


urlpatterns = [
    # ADMIN SITE
    path('admin/', admin.site.urls),
    # ACCOUNTS
    path('accounts/', include('accounts.urls')),
    # RECORDS
    path('records/', include('records.urls')),
    # SITES
    path('sites/', include('sites.urls')),
    # TAGS
    path('tags/', include('tags.urls')),
    # JWT
    path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/', jwt_views.TokenObtainSlidingView.as_view(), name='token_obtain'),
    path('api/token/refresh/', jwt_views.TokenRefreshSlidingView.as_view(), name='token_refresh'),
]
