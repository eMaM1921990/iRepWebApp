from iRep.models import Forms, FormQuestions, QuestionAnswer
import logging

logger = logging.getLogger(__name__)
class IForm():
    def __init__(self, slug):
        self.corp_slug = slug

    def getFormList(self):
        return Forms.objects.filter(corporate__slug=self.corp_slug)

    def getFormQuestions(self,id):
        return FormQuestions.objects.filter(form__id=id)

    def getFormInfo(self,id):
        return Forms.objects.get(id=id)


    def saveFormQuestionAnswer(self, question_id,sales_force_id, answer):
        try:
            record = QuestionAnswer()
            record.question_id = question_id
            record.sales_force_id = sales_force_id
            record.answer = answer
            record.save()
            return record
        except Exception as e:
            logging.debug('Error during save question answer cause '+str(e))
            print str(e)
            return None