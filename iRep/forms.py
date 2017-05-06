from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import ugettext_lazy as _

from iRep.models import SalesForce


class SalesForceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SalesForceForm,self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'sales-force-form-id'
        self.helper.form_method = 'post'

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit(_('Save'), _('Save')))

    class Meta:
        model = SalesForce
        exclude = ['last_activity','created_date','created_by']
