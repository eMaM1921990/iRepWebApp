from import_export import resources

from iRep.models import Visits, SalesForceSchedual, Orders, SalesForce, Client, Forms

__author__ = 'eMaM'


class VisitsResource(resources.ModelResource):
    class Meta:
        model = Visits


class SchedualResource(resources.ModelResource):
    class Meta:
        model = SalesForceSchedual


class OrderResource(resources.ModelResource):
    class Meta:
        model = Orders


class SalesForceResource(resources.ModelResource):
    class Meta:
        model = SalesForce



class ClientResource(resources.ModelResource):
    class Meta:
        model = Client


class FormResource(resources.ModelResource):
    class Meta:
        model = Forms