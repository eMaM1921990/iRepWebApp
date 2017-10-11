import datetime
from crispy_forms.bootstrap import PrependedText, AppendedText, Accordion, AccordionGroup, FieldWithButtons, \
    StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Field, Fieldset, Div, HTML, Button
from django import forms
from django.forms.formsets import BaseFormSet
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from iRep.api import Clients
from iRep.managers.Products import ProductManager
from iRep.managers.Tags import TagManager
from iRep.models import SalesForce, ProductGroup, Product, Corporate, UserProfile, Client, Forms, FormQuestions, \
    BillBoard


class SignupForm(forms.Form):
    name = forms.CharField(max_length=30, label=_('Name'),
                           widget=forms.TextInput(attrs={'placeholder': _(' Name')}), required=False)
    email = forms.CharField(max_length=64, label=_('Email'),
                            widget=forms.TextInput(attrs={'placeholder': _('E-mail address')}))
    address = forms.CharField(max_length=150, label=_('Address'),
                              widget=forms.TextInput(attrs={'placeholder': _('Address')}))
    mobile = forms.CharField(max_length=150, label=_('Phone'),
                             widget=forms.TextInput(attrs={'placeholder': _('Phone')}))
    corp_admin = forms.CharField(max_length=150, label=_('Corporate Admin'),
                                 widget=forms.TextInput(attrs={'placeholder': _('Corporate Admin')}))
    corp_admin_phone = forms.CharField(max_length=150, label=_('Corporate Admin Phone'),
                                       widget=forms.TextInput(attrs={'placeholder': _('Corporate Admin Phone')}))

    # def raise_duplicate_email_error(self):
    # # here I tried to override the method, but it is not called
    #     raise forms.ValidationError(
    #         _("An account already exists with this e-mail address."
    #           " Please sign in to that account."))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['name']
        user.last_name = ''
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.save()
        # save corp
        corp = Corporate()
        corp.corporate_name = user.first_name
        corp.corporate_address_txt = self.cleaned_data['address']
        corp.mobile = self.cleaned_data['mobile']
        corp.email = self.cleaned_data['email']
        corp.admin_name = self.cleaned_data['corp_admin']
        corp.admin_mobile = self.cleaned_data['corp_admin_phone']
        corp.created_by = user
        corp.slug = slugify('%s %s' % (user.get_full_name(), user.id), allow_unicode=True)
        corp.save()
        # save profile
        profile = UserProfile()
        profile.auth_user = user
        profile.corporate = corp
        profile.user_type = 1
        profile.save()


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
        corp_instance = kwargs.pop('corp_instance', None)
        action = kwargs.pop('action', None)
        super(SalesForceForm, self).__init__(*args, **kwargs)
        # init data
        if corp_instance:
            self.fields['company_id'].initial = corp_instance.slug
            self.fields['report_to'].queryset = SalesForce.objects.filter(corp_id=corp_instance)
        # self.fields['user_pin'].initial = user_instance.id
        # control Required
        self.fields['avatar'].required = False
        self.fields['name'].required = True
        self.fields['password_pin'].required = True
        self.fields['user_pin'].required = True
        self.fields['notes'].required = False
        self.fields['company_id'].required = True
        self.fields['position'].required = True
        self.fields['report_to'].required = False

        # control readOnly
        self.fields['company_id'].widget.attrs['readonly'] = True
        self.fields['user_pin'].widget.attrs['readonly'] = False

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
        self.fields['report_to'].label = _('Reporting to')
        self.fields['serial_number'].label = _('Serial number')

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
                        Field('report_to', empty_label=_('Reporting to')),
                        css_class='col-md-6'
                    ),
                    Div(css_class='clearfix'),

                    Div(Fieldset(_('Activation Data'),
                                 PrependedText('company_id', '<i class="fa fa-building" aria-hidden="true"></i>',
                                               css_class='col-md-6', placeholder=_('Company ID')),
                                 PrependedText('user_pin', '<i class="fa fa-user" aria-hidden="true"></i>',
                                               css_class='col-md-6', placeholder=_('App UserID')),
                                 PrependedText('password_pin', '<i class="fa fa-key" aria-hidden="true"></i>',
                                               css_class='col-md-6',
                                               placeholder=_('App Password')),

                                 PrependedText('serial_number', '<i class="fa fa-key" aria-hidden="true"></i>',
                                               css_class='col-md-6',
                                               placeholder=_('Device Serial')),
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
            ))

    # override save form
    def save(self, user, commit=True):
        m = super(SalesForceForm, self).save(commit=False)
        m.corp_id = Corporate.objects.get(slug=self.cleaned_data['company_id'])
        m.created_by = user
        m.slug = slugify('%s %s' % (m.name, user.id), allow_unicode=True)
        m.save()
        return m

    class Meta:
        model = SalesForce
        exclude = ['last_activity', 'created_date', 'created_by', 'corp_id', 'slug']


class SalesForceReportForm(BaseReportForm):
    sales_force = forms.CharField()

    def __init__(self, *args, **kwargs):
        sales_force_id = kwargs.pop('sales_force', None)
        super(SalesForceReportForm, self).__init__(*args, **kwargs)
        # initial
        self.fields['date_from'].initial = datetime.datetime.today()
        self.fields['date_to'].initial = datetime.datetime.today()
        self.fields['sales_force'].widget = forms.HiddenInput()
        if sales_force_id:
            self.fields['sales_force'].initial = str(sales_force_id)

        # override label
        self.fields['date_from'].label = ''
        self.fields['date_to'].label = ''
        # self.fields['static_range'].label = ''

        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'sales-force-form-report-id'
        self.helper.form_method = 'post'
        self.helper.form_action = None
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
                Button(_('Apply'), _('Apply'), css_class='bbtn btn-primary btn-md'),
                css_class='col-md-3'
            ),
            Field('sales_force')

        )


class ClientReportForm(BaseReportForm):
    client_id = forms.CharField()

    def __init__(self, *args, **kwargs):
        client_id = kwargs.pop('client', None)
        super(ClientReportForm, self).__init__(*args, **kwargs)
        # initial
        self.fields['date_from'].initial = datetime.datetime.today()
        self.fields['date_to'].initial = datetime.datetime.today()
        self.fields['client_id'].widget = forms.HiddenInput()
        if client_id:
            self.fields['client_id'].initial = str(client_id)

        # override label
        self.fields['date_from'].label = ''
        self.fields['date_to'].label = ''
        # self.fields['static_range'].label = ''

        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'sales-force-form-report-id'
        self.helper.form_method = 'post'
        self.helper.form_action = None
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
                Button(_('Apply'), _('Apply'), css_class='bbtn btn-primary btn-md'),
                css_class='col-md-3'
            ),
            Field('client_id')

        )


class ProductCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductCategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = _('Category name')
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['is_active'].widget.attrs['data-toggle'] = 'toggle'

    def save(self, user, corporate, commit=True):
        m = super(ProductCategoryForm, self).save(commit=False)
        m.created_by = user
        m.corporate = corporate
        m.save()
        return m

    class Meta:
        model = ProductGroup
        exclude = ['created_date', 'created_by', 'corporate']


class ProductForm(forms.ModelForm):
    # tags = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        # POP from kwargs
        corpSlug = kwargs.pop('slug', None)
        # Retrieve Corp Tags
        action = kwargs.pop('action', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        # init
        self.fields['product'].queryset = ProductManager().get_corp_category(corpSlug)
        # input label
        self.fields['image'].label = _('Logo')
        self.fields['name'].label = _('Name')
        self.fields['ean_code'].label = _('EAN')
        self.fields['default_price'].label = _('Default price')
        self.fields['note'].label = _('Notes')
        self.fields['product'].label = _('Product Group')
        self.fields['unit'].label = _('Units')
        self.fields['is_active'].label = _('Is active')
        # self.fields['tags'].label = _('Tags')

        # control Required
        self.fields['image'].required = False
        self.fields['default_price'].required = True
        self.fields['corporate'].required = False
        self.fields['unit'].required = False
        self.fields['slug'].required = False
        # init
        self.fields['default_price'].initial = '0.00'
        self.fields['note'].widget.attrs['rows'] = 3
        # if tags:
        #     self.fields['tags'].queryset = tags
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'product-form-id'
        self.helper.form_method = 'post'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Field('image', css_class=''),
            Div(
                css_class='divider-md'
            ),
            Div(
                Div(

                    Div(
                        Field('name', placeholder=_('Product name')),
                        css_class='col-md-6'
                    ),

                    Div(
                        Div(
                            css_class='divider-md'
                        ),
                        Field('is_active', placeholder=_('Status')),
                        css_class='col-md-6'
                    ),
                    css_class='col-md-12'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Div(
                        Field('ean_code', placeholder=_('EAN')),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('default_price', placeholder=_('Default price')),
                        css_class='col-md-6'
                    ),
                    css_class='col-md-12'
                ),
                css_class='row'
            ),
            Div(
                css_class='divider-md'
            ),
            Div(
                Div(
                    Div(
                        Field('note', placeholder=_('Notes')),
                        css_class='col-md-6'
                    ),

                    css_class='col-md-12'
                ),
                css_class='row'
            ),
            Div(
                css_class='divider-md'
            ),
            Div(
                Div(
                    Div(
                        FieldWithButtons('product',
                                         StrictButton("Add new!", css_class=".newcategory", css_id='newCategory'),
                                         placeholder=_('Product category')),
                        css_class='col-md-6'
                    ),
                    # Div(
                    #     Div(
                    #         css_class='divider-md'
                    #     ),
                    #     Button(_('Custom Group'), _('Custom Group'), css_class="btn btn-lg btn-default"),
                    #     css_class='col-md-6'
                    # ),
                    Div(
                        css_class='clearfix'
                    ),
                    css_class='col-md-12'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    css_class='divider-lg clearfix'
                ),
                Div(
                    Reset(_('Cancel'), _('Cancel'), css_class='btn btn-default  btn-lg min-btn'),
                    Submit(_('Save'), _('Save'), css_class='btn btn-primary  btn-lg min-btn'),
                    css_class='text-center'
                ),

                css_class='row'
            )

        )

    # override save form
    def save(self, user, corporate, commit=True):
        m = super(ProductForm, self).save(commit=False)
        m.slug = slugify('%s %s' % (m.name, user.id), allow_unicode=True)
        m.corporate = corporate
        m.created_by = user
        m.save()
        return m

    class Meta:
        model = Product
        exclude = ['created_date', 'created_by']


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # POP from kwargs
        action = kwargs.pop('action', None)
        corp_instance = kwargs.pop('corp_instance', None)
        super(ClientForm, self).__init__(*args, **kwargs)
        # Input label
        self.fields['name'].label = _('Name')
        self.fields['address_txt'].label = _('Address ')
        self.fields['zipcode'].label = _('Zipcode')
        self.fields['contact_name'].label = _('Contact name')
        self.fields['contact_title'].label = _('Contant title')
        self.fields['website'].label = _('Website')
        self.fields['email'].label = _('E-mail')
        self.fields['phone'].label = _('Phone')
        self.fields['notes'].label = _('Notes')
        self.fields['status'].label = _('Status')
        self.fields['city'].label = _('City')
        self.fields['state'].label = _('State')
        self.fields['country'].label = _('Country')
        self.fields['main_branch'].label = _('Main branch')
        self.fields['is_active'].label = _('Is active')
        self.fields['sales_force'].label = _('Sales force')
        # control Required
        self.fields['name'].required = True
        self.fields['address_txt'].required = True
        self.fields['zipcode'].required = True
        self.fields['contact_name'].required = True
        self.fields['contact_title'].required = True
        self.fields['website'].required = False
        self.fields['email'].required = False
        self.fields['phone'].required = True
        self.fields['notes'].required = False
        self.fields['city'].required = True
        self.fields['state'].required = True
        self.fields['country'].required = True
        self.fields['main_branch'].required = False
        self.fields['is_active'].required = False
        self.fields['sales_force'].required = True
        self.fields['corporate'].required = False
        self.fields['avatar'].required = False
        self.fields['slug'].required = False
        # init
        self.fields['notes'].widget.attrs['rows'] = 3
        if corp_instance:
            self.fields['sales_force'].queryset = SalesForce.objects.filter(corp_id=corp_instance)

        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'client-form-id'
        self.helper.form_method = 'post'
        self.helper.form_action = action
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('name', placeholder=_('Product name')),
                    Field('sales_force', placeholder=_('Sales force')),
                    Field('phone', placeholder=_('Phone')),
                    css_class='col-md-6'
                ),
                Div(
                    Field('is_active', placeholder=_('Is active')),
                    Field('status', placeholder=_('Status')),
                    css_class='col-md-6'
                ),
                css_class='row'
            ),
            Div(
                css_class='divider-md',
            ),
            Accordion(
                AccordionGroup(
                    _('Address Info'),
                    Div(
                        Field('address_txt', placeholder=_('Address')),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('city', placeholder=_('City')),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('state', placeholder=_('State')),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('country', placeholder=_('Country')),
                        css_class='col-md-4'
                    ),
                    Div(
                        Field('zipcode', placeholder=_('Zipcode')),
                        css_class='col-md-4'
                    )

                ),
                AccordionGroup(
                    _('Contact Info'),
                    Div(
                        Field('contact_title', placeholder=_('Contact Title')),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('contact_name', placeholder=_('Contact name')),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('website', placeholder=_('Website')),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('email', placeholder=_('E-mail')),
                        css_class='col-md-6'
                    )
                )

            ),
            Div(
                Field('notes', placeholder=_('Notes')),
                css_class='col-md-6'
            ),
            Div(
                css_class='divider-lg clearfix'
            ),

            Div(
                Reset(_('Cancel'), _('Cancel'), css_class='btn btn-default  btn-lg min-btn'),
                Submit(_('Save'), _('Save'), css_class='btn btn-primary  btn-lg min-btn'),
                css_class='text-center'
            )
        )

    # override save form
    def save(self, user, corporate, main_branch, commit=True):
        m = super(ClientForm, self).save(commit=False)
        m.created_by = user
        m.corporate = corporate
        if main_branch:
            m.main_branch_id = main_branch
        m.slug = slugify('%s %s' % (m.name, user.id), allow_unicode=True)
        m.save()
        return m

    class Meta:
        model = Client
        exclude = ['created_date', 'created_by']


class TrackingVisitFormByClient(BaseReportForm):
    clients = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super(TrackingVisitFormByClient, self).__init__(*args, **kwargs)
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


class QuestionForm(forms.Form):
    question = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your questions'),
            'class': 'form-control',
            'aria-describedby': 'basic-addon2'
        }),
        required=True)

    # class Meta:
    #     model = FormQuestions
    #     exclude = ['created_date', 'form']


class FormsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.corp = kwargs.pop('corp', None)
        super(FormsForm, self).__init__(*args, **kwargs)
        self.fields['form_name'] = forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={
                'placeholder': _('Form name'),
                'class': 'form-control sizeinput-int'
            }))
        self.fields['description'] = forms.CharField(
            max_length=30,
            widget=forms.Textarea(attrs={
                'placeholder': _('Description'),
                'class': 'form-control'
            }))
        self.fields['is_active'] = forms.BooleanField(
            widget=forms.CheckboxInput()
        )
        self.fields['is_active'].label = _('Is active')

    def save(self, commit=True):
        m = super(FormsForm, self).save(commit=False)
        # m.form_name = self.cleaned_data['form_name']
        # m.description = self.cleaned_data['description']
        # m.is_active = self.cleaned_data['is_active']
        m.corporate = self.corp
        m.save()
        return m

    class Meta:
        model = Forms
        exclude = ['created_date', 'corporate']


class BaseQuestionFormSet(BaseFormSet):
    def clean(self):
        """
               Adds validation to check that no two links have the same anchor or URL
               and that all links have both an anchor and URL.
               """
        if any(self.errors):
            return

        questions = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                question = form.cleaned_data['question']

                # Check that no two links have the same anchor or URL
                if question:
                    if question in questions:
                        duplicates = True
                    questions.append(question)

                if duplicates:
                    raise forms.ValidationError(
                        'Question must have unique ',
                        code='duplicate_question'
                    )

                if not question:
                    raise forms.ValidationError(
                        'All links must have a URL.',
                        code='missing_question'
                    )


class BillBoardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # POP from kwargs
        action = kwargs.pop('action', None)
        super(BillBoardForm, self).__init__(*args, **kwargs)
        # Input label
        self.fields['subject'].label = _('Subject')
        self.fields['body'].label = _('Note ')

        # control Required
        self.fields['subject'].required = True
        self.fields['body'].required = True

        # init
        self.fields['body'].widget.attrs['rows'] = 3

        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'billboard-form-id'
        self.helper.form_method = 'post'
        self.helper.form_action = action

        self.helper.layout = Layout(
            Div(
                css_class='clearfix'
            ),
            Div(
                css_class='divider-md'
            ),
            Div(
                Div(
                    Field('subject', placeholder=_('Subject')),
                    css_class='form-group'
                ),
                Div(
                    Field('body', placeholder=_('Note')),
                    css_class='form-group'
                ),
                Div(
                    Reset(_('Cancel'), _('Cancel'), css_class='btn btn-default  btn-lg min-btn'),
                    Submit(_('Save'), _('Save'), css_class='btn btn-primary  btn-lg min-btn'),
                    css_class='text-center divider-lg'
                )
            )
        )

    def save(self, user,corporte, commit=True):
        m = super(BillBoardForm, self).save(commit=False)
        m.created_by = user
        m.corporate = corporte
        m.is_active= True
        m.save()
        return m

    class Meta:
        model = BillBoard
        exclude = ['created_date','corporate','is_active','created_by']