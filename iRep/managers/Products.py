from iRep.models import Product
import logging

logger = logging.getLogger(__name__)


class ProductManager():
    def get_corp_products(self, slug):
        try:
            Product.objects.filter(corporate__slug=slug)
        except Exception as e:
            logger.debug('Error during retrieve products for company slug ' + str(slug) + ' cause: ' + str(e))
