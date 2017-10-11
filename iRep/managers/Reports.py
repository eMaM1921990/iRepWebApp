from django.conf.global_settings import DATE_FORMAT, DATE_INPUT_FORMATS
from django.db.models import Count, Sum, fields
from django.db.models import ExpressionWrapper
from django.db.models import F
import datetime
from iRep.models import SalesForceCheckInOut, Visits, Orders, SalesForceTimeLine, SalesForceTrack, Client, \
    SalesForceSchedual

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

    def visits_by_client_count(self, client_id):
        return SalesForceCheckInOut.objects.prefetch_related().filter(branch__id=client_id,
                                                                      check_in_date__lte=self.to_date,
                                                                      check_in_date__gte=self.from_date).count()

    def countTotalPlaceVisited(self, sales_force_id):
        return Visits.objects.filter(sales_force__id=sales_force_id, visit_date__lte=self.to_date,
                                     visit_date__gte=self.from_date).count()

    def countNumberOfOrders(self, sales_force_id):
        return Orders.objects.filter(sales_force__id=sales_force_id).count()

    def countNumberOfOrdersByClient(self, client_id):
        return Orders.objects.filter(branch__id=client_id).count()

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
        currentDate = datetime.datetime.strptime(self.from_date, DATE_INPUT_FORMATS[0])
        return SalesForceTrack.objects.filter(sales_force__corp_id=slug, created_date__day=currentDate.day,
                                              created_date__month=currentDate.month,
                                              created_date__year=currentDate.year)


class DashBoardReports():
    def __init__(self, start_date, end_date, city, corp, context):
        self.from_date = start_date
        self.to_date = end_date
        self.city = city
        self.corp = corp
        self.context = context

    def get_dashboard_statistics(self):
        self.context['activeRep'] = self.get_active_salesforce_count()
        self.context['clientCount'] = self.get_create_clients_count()
        self.context['total_order'] = self.get_total_orders()
        self.context['total_amount'] = self.get_total_amount()
        self.context['totalSchedual'] = self.get_total_schedual()
        self.context['totalVisit'] = self.get_total_visits()
        self.context['missed'] = self.context['totalSchedual'] - self.context['totalVisit']
        self.context['follow_up'] = self.get_follow_up_client()
        self.context['new_client'] = self.get_new_client

    def get_active_salesforce_count(self):
        return SalesForceTimeLine.objects.filter(time_line_date=self.from_date, end_time__isnull=True,
                                                 sales_force__corp_id=self.corp).count()

    def get_create_clients_count(self):
        start_date = datetime.datetime.strptime(self.from_date, DATE_INPUT_FORMATS[0])
        return Client.objects.filter(created_date__day=start_date.day,
                                     created_date__month=start_date.month,
                                     created_date__year=start_date.year, corporate=self.corp).count()

    def get_total_orders(self):
        start_date = datetime.datetime.strptime(self.from_date, DATE_INPUT_FORMATS[0])
        return Orders.objects.filter(sales_force__corp_id=self.corp, order_date__day=start_date.day,
                                     order_date__month=start_date.month, order_date__year=start_date.year).count()

    def get_total_amount(self):
        start_date = datetime.datetime.strptime(self.from_date, DATE_INPUT_FORMATS[0])
        return (Orders.objects.filter(sales_force__corp_id=self.corp, order_date__day=start_date.day,
                                      order_date__month=start_date.month, order_date__year=start_date.year).aggregate(
            Sum('total')))['total__sum']

    def get_visit_details_charts(self):
        return Visits.objects.filter(visit_date__lte=self.to_date, visit_date__gte=self.from_date,
                                     sales_force__corp_id=self.corp).values('visit_date').annotate(
            totalVisit=Count('visit_date')
        )

    def get_total_orders_chart(self):
        return Orders.objects.filter(order_date__lte=self.to_date, order_date__gte=self.from_date,
                                     sales_force__corp_id=self.corp).values('order_date').annotate(
            totalOrder=Count('order_date'), totalAmount=Sum('total')
        )

    def get_total_schedual(self):
        return SalesForceSchedual.objects.filter(schedual_date__lte=self.to_date, schedual_date__gte=self.from_date,
                                                 sales_force__corp_id=self.corp).count()

    def get_total_visits(self):
        return Visits.objects.filter(visit_date__lte=self.to_date, visit_date__gte=self.from_date,
                                     sales_force__corp_id=self.corp).count()

    def get_follow_up_client(self):
        return Orders.objects.filter(order_date__lte=self.to_date, order_date__gte=self.from_date,
                                     sales_force__corp_id=self.corp).count()

    def get_qualificed_client(self):
        return Visits.objects.filter(visit_date__lte=self.to_date, visit_date__gte=self.from_date,
                                     sales_force__corp_id=self.corp)

    def get_new_client(self):
         visit = Visits.objects.filter(visit_date__lte=self.to_date, visit_date__gte=self.from_date,
                              sales_force__corp_id=self.corp)

         return Client.objects.all().exclude(id__in = [v.branch.id for v in visit])
