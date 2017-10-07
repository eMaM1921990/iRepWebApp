from iRep.models import BillBoard
import datetime

__author__ = 'eMaM'


class BillBoards:
    def __init__(self, slug):
        self.slug = slug

    def list(self):
        return BillBoard.objects.filter(corporate__slug=self.slug)

    def getBillBoards(self, id):
        return BillBoard.objects.get(id=id)

    def listToday(self):
        currentDate = datetime.datetime.today().strftime('%Y-%m-%d')
        return BillBoard.objects.filter(corporate__slug=self.slug, created_date__day=currentDate.day,
                                        created_date__month=currentDate.month, created_date__year=currentDate.year)
