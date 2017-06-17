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
            logging.debug('Error during save schedual cause :'+str(e))
            return None