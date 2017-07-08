from iRep.models import Orders

__author__ = 'eMaM'
import logging

logger = logging.getLogger(__name__)


class OrderManager():
    def save_order(self, sales_force_id, branch_id, order_date, total, sub_total, discount, visit_id, notes, items):
        try:
            record = Orders()
            record.sales_force_id = sales_force_id
            record.branch_id = branch_id
            record.order_date = order_date
            record.total = total
            record.sub_total = sub_total
            record.discount = discount
            record.created_form_visit_id = visit_id
            record.notes = notes
            record.save()
            for item in items:
                record.order_lines.create(
                    product_id=item['product_id'],
                    price=item['item_price'],
                    quantity=item['quantity']
                )
            return record
        except Exception as e:
            logging.error('error during save order for sales_force_id' + str(sales_force_id) + ' cause: ' + str(e))
            return None
