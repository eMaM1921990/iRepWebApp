# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from iRep.models import SalesForceCategory, ProductGroup, Product, ProductUnit, AppLanguage, Client

admin.site.register(SalesForceCategory)
admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(ProductUnit)
admin.site.register(AppLanguage)
admin.site.register(Client)