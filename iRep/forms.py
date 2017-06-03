import datetime
from crispy_forms.bootstrap import PrependedText, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Field, Fieldset, Div, HTML, Button
from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from iRep.managers.Tags import TagManager
from iRep.models import SalesForce, ProductGroup, Product, Corporate, UserProfile


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
        self.fields['company_id'].initial = corp_instance.slug
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
                                 PrependedText('company_id', '<i class="fa fa-building" aria-hidden="true"></i>',
                                               css_class='col-md-6', placeholder=_('Company ID')),
                                 PrependedText('user_pin', '<i class="fa fa-user" aria-hidden="true"></i>',
                                               css_class='col-md-6', placeholder=_('App UserID')),
                                 PrependedText('password_pin', '<i class="fa fa-key" aria-hidden="true"></i>',
                                               css_class='col-md-6',
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


class ProductCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductCategoryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ProductGroup
        exclude = ['created_date', 'created_by']


class ProductForm(forms.ModelForm):
    tags = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        # POP from kwargs
        corpSlug = kwargs.pop('slug', None)
        # Retrieve Corp Tags
        tags = TagManager().get_corp_tags(corpSlug)
        action = kwargs.pop('action', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        # input label
        self.fields['name'].label = _('Name')
        self.fields['ean_code'].label = _('EAN')
        self.fields['default_price'].label = _('Default price')
        self.fields['note'].label = _('Notes')
        self.fields['product'].label = _('Product Group')
        self.fields['unit'].label = _('Units')
        self.fields['is_active'].label = _('Is active')
        self.fields['tags'].label = _('Tags')

        # control Required
        self.fields['default_price'].required = True
        self.fields['corporate'].required = False
        self.fields['unit'].required = False
        self.fields['slug'].required = False
        # init
        self.fields['default_price'].initial = '0.00'
        self.fields['note'].widget.attrs['rows'] = 3
        if tags:
            self.fields['tags'].queryset = tags
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        self.helper.form_id = 'product-form-id'
        self.helper.form_method = 'post'
        self.helper.form_action = action
        self.helper.layout = Layout(
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
                    Div(
                        Field('tags', placeholder=_('Tags')),
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
                        Field('product', placeholder=_('Product category')),
                        css_class='col-md-6'
                    ),
                    Div(
                        Div(
                            css_class='divider-md'
                        ),
                        Button(_('Custom Group'), _('Custom Group'), css_class="btn btn-lg btn-default"),
                        css_class='col-md-6'
                    ),
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
    def save(self, user,corporate, commit=True):
        m = super(ProductForm, self).save(commit=False)
        m.slug = slugify('%s %s' % (m.name, user.id), allow_unicode=True)
        m.corporate = corporate
        m.created_by = user
        m.save()
        # Save Tags
        m.tag_product.create(tag__id=self.cleaned_data['tags'])
        return m

    class Meta:
        model = Product
        exclude = ['created_date', 'created_by']
