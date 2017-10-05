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

from iRep import views, api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/', include('allauth.urls')),  # All auth
    url(r'^$', views.home, name='index'),
    # Localizations #
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # serve media
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
]

urlpatterns += [
    # sales force
    url(r'^salesForce/add/$', views.AddSalesForce, name='createSalesForce'),
    url(r'^(?P<slug>[-\w]+)/salesForce/list/$', views.ViewSalesForceDefault, name='viewSalesForceByUser'),
    url(r'^salesForce/edit/(?P<slug>[-\w]+)/', views.EditSalesForce, name='editSalesForce'),
    # Products
    url(r'^settings/(?P<slug>[-\w]+)/product/add/$', views.AddProduct, name='createProduct'),
    url(r'^settings/(?P<slug>[-\w]+)/product/list/$', views.ViewProduct, name='productList'),
    url(r'^settings/product/(?P<slug>[-\w]+)/$', views.ViewEditProduct, name='editProduct'),
    url(r'^settings/category/add/$', views.AddCategory, name='AddCategory'),
    # Clients
    url(r'^client/(?P<slug>[-\w]+)/$', views.ViewClient, name='viewClient'),
    url(r'^client/edit/(?P<slug>[-\w]+)/$', views.EditClient, name='EditClient'),
    url(r'^client/(?P<slug>[-\w]+)/add/$', views.AddClient, name='AddClient'),
    url(r'^orders/(?P<slug>[-\w]+)/$', views.viewOrder, name='viewOrder'),
    # schedual
    url(r'^scheduler/add/$', views.AddScheduler, name='AddScheduler'),

    # Froms
    url(r'^forms/(?P<slug>[-\w]+)/$', views.ViewForms, name='ViewForms'),
    url(r'^addForms/(?P<slug>[-\w]+)/add$', views.CreateForms, name='addForms'),
    url(r'^Forms/edit/(?P<slug>[-\w]+)/(?P<id>[-\w]+)', views.EditForms, name='editForms'),

    # Bill Board
    url(r'^billboard/(?P<slug>[-\w]+)/', views.billBoards, name='billBoards'),
    url(r'^newBillBoard/', views.newBillBoard, name='newBillBoards'),
    url(r'^editbillBoard/(?P<id>.+)/$', views.editBillBoard, name='editBillBoard'),
    # Report
    url(r'^report/visit_tracking_by_sales_force/$', views.TrackingVisitReportBySalesForce,
        name='TrackingVisitReportBySalesForce'),
]

urlpatterns += [
    # API
    url(r'^api/v1/login/$', api.SalesForceLogin, name='apiLogin'),
    url(r'^api/v1/salesfunnel/$', api.GetSalesFunnel, name='apiGetSalesFunnel'),
    url(r'^api/v1/catalog/(?P<slug>.+)/$', api.ProductCategory, name='apiProductCatalaog'),
    url(r'^api/v1/clients/(?P<slug>.+)/$', api.Clients, name='apiClients'),
    url(r'^api/v1/client/add/$', api.AddClient, name='apiAddClients'),
    url(r'^api/v1/client/orders/(?P<clientId>.+)/$', api.ClientsOrder, name='apiClientsOrder'),
    url(r'^api/v1/client/order/add/$', api.OrderCreate, name='apiOrderCreate'),

    url(r'^api/v1/schedual/sf/(?P<sales_force_id>.+)/$', api.ListSchedualerBySF, name='apiCorpSchedualBySF'),
    url(r'^api/v1/schedual/cl/(?P<client_id>.+)/$', api.ListSchedualerByCL, name='apiCorpSchedualByCL'),
    url(r'^api/v1/schedual/add/$', api.addSchedual, name='apiCorpSchedualAdd'),

    url(r'^api/v1/working/start/$', api.SalesForceTimeLineStart, name='apiSalesForceTimeLineStart'),
    url(r'^api/v1/working/end/$', api.SalesForceTimeLineEnd, name='apiSalesForceTimeLineEnd'),
    url(r'^api/v1/check/in/$', api.CheckIn, name='apiCheckIn'),
    url(r'^api/v1/check/out/$', api.CheckOut, name='apiCheckOut'),
    url(r'^api/v1/tracking/$', api.Track, name='apiTrack'),

    url(r'^api/v1/tags/(?P<slug>.+)/$', api.ListTags, name='apiListTags'),

    url(r'^api/v1/forms/(?P<slug>.+)/$', api.ListForms, name='apiListForms'),
    url(r'^api/v1/question_answer/$', api.QuestionAnswer, name='apiQuestionAnswer'),


    # serve media
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),

]

