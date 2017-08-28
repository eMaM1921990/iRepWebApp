from iRep.models import SalesForceCheckInOut, Visits

__author__ = 'eMaM'


class TrackingReports():
    def __init__(self, start_date, end_date):
        self.from_date = start_date
        self.to_date = end_date

    def visits_by_sales_force(self, sales_force_id):
        return SalesForceCheckInOut.objects.prefetch_related().filter(sales_force__id=sales_force_id,
                                                                      check_in_date__lte=self.to_date,
                                                                      check_in_date__gte=self.from_date)

    def visits_by_client(self, client_id):
        return SalesForceCheckInOut.objects.prefetch_related().filter(branch__id=client_id,
                                                                      check_in_date__lte=self.to_date,
                                                                      check_in_date__gte=self.from_date)

    def countTotalPlaceVisited(self, sales_force_id):
        return Visits.objects.filter(sales_force__id=sales_force_id,visit_date__lte=self.from_date,visit_date__gte=self.to_date)


