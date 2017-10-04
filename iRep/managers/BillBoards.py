__author__ = 'eMaM'

class BillBoard:

    def __init__(self, slug):
        self.slug = slug

    def list(self):
        return BillBoard.objects.filter(corporate__slug=self.slug)