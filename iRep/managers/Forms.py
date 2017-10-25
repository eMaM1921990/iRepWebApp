from iRep.models import Forms, FormQuestions, QuestionAnswer
import logging

logger = logging.getLogger(__name__)


class IForm():
    def __init__(self, slug):
        self.corp_slug = slug
        
    def deleteForm(self,id):
        try:
            Forms.objects.get(id=id).delete()
            return True
        except Exception as e:
            print str(e)
            return None

    def getFormList(self):
        return Forms.objects.filter(corporate__slug=self.corp_slug)

    def getFormQuestions(self, id):
        return FormQuestions.objects.filter(form__id=id)

    def getFormInfo(self, id):
        return Forms.objects.get(id=id)

    def saveFormQuestionAnswer(self, question_id, sales_force, answer, visit_id, branch_id):
        try:
            record = QuestionAnswer()
            record.question_id = question_id
            record.sales_force_id = sales_force
            record.answer = answer
            record.visit_id = visit_id
            record.branch_id= branch_id
            record.save()
            return record
        except Exception as e:
            logging.debug('Error during save question answer cause ' + str(e))
            print str(e)
            return None

    def getFormQuestionAnswer(self, id,branch):
        return QuestionAnswer.objects.filter(question__form__id=id,branch__id=branch)


    def getFormQuestionAnswerVisit(self, visit_id):
        return QuestionAnswer.objects.filter(visit__id=visit_id)
