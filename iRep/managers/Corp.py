from iRep.models import Corporate, UserProfile


class CorpManager():

    def get_corp_by_user(self,user):
        return Corporate.objects.get(created_by=user)

    def get_corp_form_user_profile(self,user):
        try:
            return UserProfile.objects.get(auth_user=user)
        except Exception as e:
            print str(e)
