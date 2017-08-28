from iRep.models import Forms, FormQuestions


class IForm():
    def __init__(self, slug):
        self.corp_slug = slug

    def getFormList(self):
        return Forms.objects.filter(corporate__slug=self.corp_slug)

    def getFormQuestions(self,id):
        return FormQuestions.objects.filter(form__id=id)
