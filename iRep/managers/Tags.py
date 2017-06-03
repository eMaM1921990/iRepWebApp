from iRep.models import Tags

__author__ = 'eMaM'
import logging

logger = logging.getLogger(__name__)


class TagManager():
    def get_corp_tags(self, slug):
        try:
            return Tags.objects.filter(corporate__slug=slug, is_active=True)
        except Exception as e:
            logger.debug('Error during retrieve corp tags for slug ' + str(slug) + ' cause: ' + str(e))
