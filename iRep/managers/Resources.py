from import_export import resources

from iRep.models import Visits, SalesForceSchedual, Orders

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
