# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from iRep.models import SalesForceCategory, ProductGroup, Product, ProductUnit, AppLanguage, Client, SalesFunnelStatus, \
    SalesForce, SalesForceTrack, SalesForceCheckInOut, Tags, Forms, Orders, OrderLine

admin.site.register(SalesForceCategory)
admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(ProductUnit)
admin.site.register(AppLanguage)
admin.site.register(Client)
admin.site.register(SalesFunnelStatus)
admin.site.register(SalesForce)
admin.site.register(SalesForceTrack)
admin.site.register(SalesForceCheckInOut)
admin.site.register(Tags)
admin.site.register(Forms)
admin.site.register(Orders)
admin.site.register(OrderLine)