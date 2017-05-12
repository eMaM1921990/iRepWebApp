import datetime
from crispy_forms.bootstrap import PrependedText, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Field, Fieldset, Div, HTML
from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from iRep.models import SalesForce


class BaseReportForm(forms.Form):
    report_date = [(0, _('Today')), (1, _('Yesterday')), (7, _('This week')), (14, _('Last Week')),
                   (30, _('This month')), (60, _('Last month')), (365, _('This year')), (730, _('This year'))]
    date_from = forms.DateField()
    date_to = forms.DateField()
    static_range = forms.ChoiceField(choices=report_date)


class SalesForceForm(forms.ModelForm):
    company_id = forms.CharField()

    def __init__(self, *args, **kwargs):
        # Get data from kwargs
        user_instance = kwargs.pop('user_instance', None)
        action = kwargs.pop('action', None)
        super(SalesForceForm, self).__init__(*args, **kwargs)
        # init data
        self.fields['company_id'].initial = user_instance.id
        self.fields['user_pin'].initial = user_instance.id
        # control Required
        self.fields['avatar'].required = False
        self.fields['name'].required = True
        self.fields['password_pin'].required = False
        self.fields['user_pin'].required = False
        self.fields['notes'].required = False
        self.fields['company_id'].required = False
        self.fields['position'].required = True

        # control readOnly
        self.fields['company_id'].widget.attrs['readonly'] = True
        self.fields['user_pin'].widget.attrs['readonly'] = True

        # input name
        self.fields['avatar'].label = _('Upload Image')
        self.fields['name'].label = _('Name')
        self.fields['phone'].label = _('Phone')
        self.fields['email'].label = _('E-mail')
        self.fields['profile_language'].label = _('Profile Language')
        self.fields['user_pin'].label = _('App UserID')
        self.fields['password_pin'].label = _('App Password')
        self.fields['notes'].label = _('Notes')
        self.fields['is_active'].label = _('active sales force')
        self.fields['company_id'].label = _('Company ID')
        self.fields['position'].label = _('Position')

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'sales-force-form-id'
        self.helper.form_method = 'post'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Field('avatar', css_class=''),
            Div(css_class='clearfix'),
            Div(css_class='divider-lg'),
            Div(
                Div(
                    Div(
                        Field('name', placeholder=_('Enter sales force name')),
                        Field('phone', placeholder=_('Enter phone number')),
                        Field('email', placeholder=_('Enter e-mail address')),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('position', empty_label=_('Enter e-mail address')),
                        Field('profile_language', empty_label=_('Select profile language')),
                        Field('is_active'),
                        css_class='col-md-6'
                    ),
                    Div(css_class='clearfix'),

                    Div(Fieldset(_('Activation Data'),
                                 PrependedText('company_id', '#', css_class='col-md-6', placeholder=_('Company ID')),
                                 PrependedText('user_pin', '#', css_class='col-md-6', placeholder=_('App UserID')),
                                 PrependedText('password_pin', '#', css_class='col-md-6',
                                               placeholder=_('App Password')),
                                 ),
                        css_class='col-md-6')
                    ,

                    Div(
                        Fieldset(_('Other'), Field('notes', placeholder=_('Write some notes about sales force'))),
                        css_class='col-md-6')
                    ,
                    Div(
                        Reset(_('Cancel'), _('Cancel'), css_class='btn btn-default  btn-lg min-btn'),
                        Submit(_('Save'), _('Save'), css_class='btn btn-primary  btn-lg min-btn'),
                        css_class='text-center'
                    ),
                    css_class='panel-body'
                ),
                css_class='panel panel-default'
            ),

        )

    # override save form
    def save(self, user, commit=True):
        m = super(SalesForceForm, self).save(commit=False)
        m.corp_id_id = self.cleaned_data['company_id']
        m.created_by = user
        m.slug = slugify('%s %s' % (m.name, user.id), allow_unicode=True)
        m.save()
        return m

    class Meta:
        model = SalesForce
        exclude = ['last_activity', 'created_date', 'created_by', 'corp_id', 'slug']


class SalesForceReportForm(BaseReportForm):
    def __init__(self, *args, **kwargs):
        super(SalesForceReportForm, self).__init__(*args, **kwargs)
        # initial
        self.fields['date_from'].initial = datetime.datetime.today()
        self.fields['date_to'].initial = datetime.datetime.today()

        # override label
        self.fields['date_from'].label = ''
        self.fields['date_to'].label = ''
        self.fields['static_range'].label = ''

        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'sales-force-form-id'
        self.helper.form_method = 'post'
        self.helper.form_action = 'javascript:add()'
        self.helper.layout = Layout(
            Div(
                AppendedText('date_from',
                             '<span class="glyphicon glyphicon-calendar"></span>',
                             placeholder=_('Start date'))
                , css_class='col-md-3'
            ),
            Div(
                AppendedText('date_to',
                             '<span class="glyphicon glyphicon-calendar"></span>',
                             placeholder=_('Start date'))
                , css_class='col-md-3'
            ),
            Div(
                Field('static_range', placeholder=_('Start date'))
                , css_class='col-md-3'
            ),
            Div(
                Submit(_('Apply'), _('Apply'), css_class='bbtn btn-primary btn-md'),
                css_class='col-md-3'
            )

        )
