import logging

from django.utils.text import slugify

from iRep.models import Client, Corporate

logger = logging.getLogger(__name__)


class ClientManager():
    def get_client_by_slug(self, slug):
        try:
            return Client.objects.filter(corporate__slug=slug)
        except Exception as e:
            logger.debug('Error during retrieve client for corp slug ' + str(slug) + ' Cause: ' + str(e))
            return None

    def CreateClientFromAPI(self, name, address_txt, zipcode, contact_name, contact_title, website, email, phone, notes,
                            corporate, status, city, state, country, sales_force):
        try:
            record = Client()
            record.name = name
            record.address_txt = address_txt
            record.zipcode = zipcode
            record.contact_name = contact_name
            record.contact_title = contact_title
            record.website = website
            record.email = email
            record.phone = phone
            record.notes = notes
            record.corporate = Corporate.objects.get(slug=corporate)
            record.status_id = status
            record.city = city
            record.state = state
            record.country = country
            record.sales_force_id = sales_force
            record.created_by_id = 1
            record.slug = slugify('%s %s' % (name, 1), allow_unicode=True)
            record.save()
            return record

        except Exception as e:
            print 'Error during add new client from mobile cause ' + str(e)
            logger.debug('Error during add new client from mobile cause ' + str(e))

    def get_client_by_sales_force(self, slug):
        try:
            return Client.objects.filter(sales_force__slug=slug)

        except Exception as e:
            logger.debug('Error during retrieve saleforce ' + str(slug) + ' clients cause ' + str(e))
            return None
