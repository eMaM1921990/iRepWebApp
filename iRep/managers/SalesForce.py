from iRep.models import SalesForce, UserProfile, SalesForceTimeLine, SalesForceCheckInOut


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

    def ListByUserCorp(self, slug):
        return SalesForce.objects.filter(corp_id__slug=slug)

    def AddSalesForceTimeLine(self, sales_force, timeLineDate, startTime, endTime, km, hours):
        record = SalesForceTimeLine(
            sales_force_id=sales_force,
            time_line_date=timeLineDate,
            start_time=startTime,
            end_time=endTime,
            km=km,
            hours=hours
        )

        record.save()
        return record


    def update_sales_force_timeline(self,id,endTime, km, hours):
        try:
            record = SalesForceTimeLine.objects.get(id=id)
            record.end_time = endTime
            record.km = km
            record.hours = hours
            record.save()
            return record

        except Exception as e:
            print str(e)
            return None


    def CheckInOut(self,sales_force,latitude,longtude,check_date,check_time,branch,visit):
        try:

            record  = SalesForceCheckInOut(
                sales_force_id=sales_force,
                latitude=latitude,
                longtude=longtude,
                check_date=check_date,
                check_time=check_time,
                branch_id=branch,
                visit=visit
            )
            record.save()
            return record
        except Exception as e:
            return None
