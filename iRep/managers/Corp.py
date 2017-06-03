from iRep.models import Corporate


class CorpManager():

    def get_corp_by_user(self,user):
        return Corporate.objects.get(created_by=user)