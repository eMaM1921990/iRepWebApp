from iRep.models import SalesForce, UserProfile


class SalesForceManager():
    def createSalesForce(self, avatar, name, phone, email, profile_language, corp_id, user_pin, password_pin, notes,
                         is_active, auth_user):
        record = SalesForce()
        if avatar:
            record.avatar = avatar
        record.name = name
        record.phone = phone
        record.email = email
        record.profile_language_id = profile_language
        record.corp_id_id = corp_id
        record.user_pin = user_pin
        record.password_pin = password_pin
        if notes:
            record.notes
        record.is_active = is_active
        record.created_by = auth_user
        record.save()

    def ListByUser(self, auth_user):
        auth_use_profile = UserProfile.objects.get(auth_user=auth_user)
        return self.ListByUserCorp(auth_use_profile.corporate_id)

    def ListByUserCorp(self, corpId):
        return SalesForce.objects.filter(corp_id__id=corpId)
