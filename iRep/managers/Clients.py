import logging

from iRep.models import Client

logger = logging.getLogger(__name__)

class ClientManager():
    def get_client_by_slug(self,slug):
        try:
            return Client.objects.filter(corporate__slug=slug)
        except Exception as e:
            logger.debug('Error during retrieve client for corp slug '+str(slug)+' Cause: '+str(e))
            return None
