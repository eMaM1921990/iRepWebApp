import logging

from iRep.models import SalesForceSchedual

logger = logging.getLogger(__name__)

__author__ = 'eMaM'


class SchedulerManager():
    def add_scheduler(self, client_id, sales_force_id, dates, times, notes):
        try:
            record = SalesForceSchedual()
            record.sales_force_id = sales_force_id
            record.branch_id = client_id
            record.schedual_date = dates
            record.schedual_time = times
            record.notes = notes
            record.save()
            return record

        except Exception as e:
            print str(e)
            logging.debug('Error during save schedual cause :'+str(e))
            return None


    def get_schedul_by_sales_force(self, sales_force):
        return SalesForceSchedual.objects.filter(sales_force__slug=sales_force)


    def get_scheduler_by_client(self, client_slug):
        return SalesForceSchedual.objects.filter(branch__slug=client_slug)

    def get_schedular(self,sales_force,branch,date):
        object = SalesForceSchedual.objects.filter(sales_force__id=sales_force,branch__id=branch,schedual_date=date)
        return object
