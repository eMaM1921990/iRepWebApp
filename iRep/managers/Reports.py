from django.db.models import Count, Sum, fields
from django.db.models import ExpressionWrapper
from django.db.models import F

from iRep.models import SalesForceCheckInOut, Visits, Orders, SalesForceTimeLine, SalesForceTrack

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
        return Visits.objects.filter(sales_force__id=sales_force_id, visit_date__lte=self.to_date,
                                     visit_date__gte=self.from_date).count()

    def countNumberOfOrders(self, sales_force_id):
        return Orders.objects.filter(sales_force__id=sales_force_id).count()

    def countTotalPlaceVisitedGroupByBranch(self, sales_force_id):
        return Visits.objects.filter(sales_force__id=sales_force_id, visit_date__lte=self.to_date,
                                     visit_date__gte=self.from_date) \
            .values('branch').annotate(totalVistitBranch=Count('branch'))

    def countSalesForceTimeAndMile(self, sales_force_id):
        return SalesForceTimeLine.objects.filter(sales_force__id=sales_force_id, time_line_date__lte=self.to_date,
                                                 time_line_date__gte=self.from_date) \
            .values('sales_force').annotate(totalKm=Sum('km'), totalHr=Sum('hours'), totalDay=Count('sales_force'))

    def countTimeinPlace(self, sales_force_id):
        duration = ExpressionWrapper(F('check_out_time') - F('check_in_time'), output_field=fields.DurationField())

        return SalesForceCheckInOut.objects.filter(sales_force__id=sales_force_id, check_in_date__lte=self.to_date,
                                                   check_in_date__gte=self.from_date).values('sales_force').annotate(
            totalTime=Sum(duration))

    def tracking_sales_force_by_corp(self, slug):
        return SalesForceTrack.objects.filter(sales_force__corp_id=slug)
