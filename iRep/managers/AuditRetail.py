from iRep.models import AuditRetails

__author__ = 'eMaM'

class AuditRetail():

    def __init__(self, slug):
        self.slug= slug

    def getAuditRetails(self):
        return AuditRetails.objects.filter(corporate__slug=self.slug)