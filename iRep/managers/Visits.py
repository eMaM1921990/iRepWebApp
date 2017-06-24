from datetime import datetime

from iRep.models import Visits

__author__ = 'eMaM'
class VisitsManager():

    def add_visit(self,sales_force,branch,visit_date,notes,schedualed,schedual):
        try:
            record = Visits()
            record.branch_id=branch
            record.sales_force_id =sales_force
            record.visit_date  = datetime.strptime(visit_date, '%Y-%m-%d')
            record.notes= notes
            record.schedualed = schedualed
            record.schedual_id = schedual
            record.save()
            return record

        except Exception as e:
            print str(e)
            return None