"""iRepWebApp URL Configuration

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
from allauth.account.views import logout
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from iRep import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/', include('allauth.urls')),  # All auth
    url(r'^$',views.home,name='index'),
    # Localizations #
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # serve media
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
]


urlpatterns +=[
    url(r'^salesForce/add/', views.AddSalesForce, name='createSalesForce'),
]