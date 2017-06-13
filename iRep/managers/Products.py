from iRep.models import Product
import logging

logger = logging.getLogger(__name__)


class ProductManager():
    def get_corp_products(self, slug):
        try:
            sqs = Product.objects.filter(corporate__slug=slug)
            return sqs
        except Exception as e:
            print 'Error during retrieve products for company slug ' + str(slug) + ' cause: ' + str(e)
            logger.debug('Error during retrieve products for company slug ' + str(slug) + ' cause: ' + str(e))
            return None
