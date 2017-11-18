import logging

import datetime

from iRep.models import SalesForceSchedual

logger = logging.getLogger(__name__)

__author__ = 'eMaM'


class SchedulerManager():
    def add_scheduler(self, client_id, sales_force_id, dates, times, notes, week, is_visit=True):
        try:
            record = SalesForceSchedual()
            record.sales_force_id = sales_force_id
            record.branch_id = client_id
            record.schedual_date = dates
            record.schedual_time = times
            record.notes = notes
            record.is_visit = is_visit
            record.save()
            if not week and len(week) > 0 and int(week) > 0:
                self.add_recuiring(object=record, week=week)
            return record

        except Exception as e:
            print str(e)
            logging.debug('Error during save schedual cause :' + str(e))
            return None


    def edit_scheduler(self, id ,client_id, sales_force_id, dates, times, notes, week, is_visit=True):
        try:
            record = SalesForceSchedual.objects.get(id=id)
            record.sales_force_id = sales_force_id
            record.branch_id = client_id
            record.schedual_date = dates
            record.schedual_time = times
            record.notes = notes
            record.is_visit = is_visit
            record.save()
            if not week and len(week) > 0 and int(week) > 0:
                self.add_recuiring(object=record, week=week)
            return record

        except Exception as e:
            print str(e)
            logging.debug('Error during update schedual cause :' + str(e))
            return None


    def delete(self, id):
        try:
            SalesForceSchedual.objects.get(id=id).delete()
            return True
        except Exception as e:
            print str(e)
            logging.debug('Error during delete schedual cause :' + str(e))
            return None




    def add_recuiring(self, object, week):
        current_date = datetime.datetime.strptime(object.schedual_date, "%Y-%m-%d")

        visit_date = current_date + datetime.timedelta(days=int(week) * 7)

        try:
            record = SalesForceSchedual()
            record.sales_force_id = object.sales_force.id
            record.branch_id = object.branch.id
            record.schedual_date = visit_date
            record.schedual_time = object.schedual_time
            record.notes = object.notes
            record.is_visit = object.is_visit
            record.save()

        except Exception as e:
            print str(e)
            logging.debug('Error during save schedual cause :' + str(e))

    def get_schedul_by_sales_force(self, sales_force):
        return SalesForceSchedual.objects.filter(sales_force__slug=sales_force)

    def get_scheduler_by_client(self, client_slug):
        return SalesForceSchedual.objects.filter(branch__slug=client_slug)

    def get_schedular(self, sales_force, branch, date):
        object = SalesForceSchedual.objects.filter(sales_force__id=sales_force, branch__id=branch, schedual_date=date)
        return object
