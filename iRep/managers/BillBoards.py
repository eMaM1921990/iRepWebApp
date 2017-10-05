from iRep.models import BillBoard

__author__ = 'eMaM'

class BillBoards:

    def __init__(self, slug):
        self.slug = slug

    def list(self):
        return BillBoard.objects.filter(corporate__slug=self.slug)

    def getBillBoards(self,id):
        return BillBoard.objects.get(id=id)