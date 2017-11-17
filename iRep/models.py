# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from cities_light.models import City, Region, Country
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from math import sin, cos, radians, degrees, acos

MANAGED = True


# Create your models here.
class Corporate(models.Model):
    avatar = models.ImageField(upload_to=settings.AVATAR_DIR, null=True, blank=True)
    corporate_name = models.CharField(max_length=150, null=False)
    corporate_address_txt = models.CharField(max_length=150, null=False)
    mobile = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=150, null=False)
    admin_name = models.CharField(max_length=150, null=False)
    admin_mobile = models.CharField(max_length=150, null=False),
    no_of_user = models.IntegerField(default=0)
    is_limited = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='corp_users', db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)

    def __unicode__(self):
        return self.corporate_name

    class Meta:
        managed = MANAGED
        db_table = 'corporates'
        verbose_name_plural = _('Corporates')
        ordering = ['-created_date']


class AppLanguage(models.Model):
    name = models.CharField(max_length=150, null=False, unique=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        managed = MANAGED
        db_table = 'app_language'


class UserProfile(models.Model):
    avatar = models.ImageField(upload_to=settings.AVATAR_DIR, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    user_type = models.IntegerField(default=0)
    digital_signature = models.ImageField(upload_to='')
    auth_user = models.ForeignKey(User, models.CASCADE, related_name='user_profile', db_column='auth_user_id')
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='user_profile_corp', db_column='corp_id')

    class Meta:
        managed = MANAGED
        db_table = 'user_profile'


class SalesFunnelStatus(models.Model):
    status_name = models.CharField(max_length=150)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)

    def __str__(self):
        return self.status_name

    def __unicode__(self):
        return self.status_name

    class Meta:
        managed = MANAGED
        db_table = 'sales_funnel_status'
        ordering = ['-created_date']


class SalesForceCategory(models.Model):
    name = models.CharField(max_length=150, null=False, unique=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = MANAGED
        db_table = 'sales_force_category'


class SalesForce(models.Model):
    avatar = models.ImageField(upload_to=settings.AVATAR_DIR)
    name = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    email = models.EmailField(null=False)
    profile_language = models.ForeignKey(AppLanguage, models.CASCADE, related_name='profile_lang',
                                         db_column='profile_lang_id')

    user_pin = models.CharField(max_length=150, null=False)
    password_pin = models.CharField(max_length=150, null=False)
    notes = models.TextField(null=True)
    corp_id = models.ForeignKey(Corporate, models.CASCADE, related_name='sales_force_corp', db_column='corp_id')
    position = models.ForeignKey(SalesForceCategory, models.DO_NOTHING, related_name='sales_force_category',
                                 db_column='position_id', null=True)
    last_activity = models.DateTimeField(default=None, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)
    report_to = models.ForeignKey('self', models.CASCADE, related_name='reporting_to', db_column='report_to', null=True)
    serial_number = models.CharField(max_length=50, null=True)

    def __str__(self):
        return "[" + self.position.name + "] " + self.name

    @property
    def getParsedQuery(self):
        txt = ''
        for field in self._meta.fields:
            txt += '[' + field.name + ':' + str(getattr(self, str(field.name))) + ']'
        return txt

    class Meta:
        managed = MANAGED
        db_table = 'sales_force'
        unique_together = ['user_pin', 'corp_id', 'name']


class Client(models.Model):
    avatar = models.ImageField(upload_to=settings.AVATAR_DIR, null=True)
    name = models.CharField(max_length=150, null=False)
    address_txt = models.CharField(max_length=200, null=False)
    zipcode = models.IntegerField()
    contact_name = models.CharField(max_length=150)
    contact_title = models.CharField(max_length=100)
    website = models.URLField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    notes = models.TextField()
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corporate_client', db_column='corp_id')
    status = models.ForeignKey(SalesFunnelStatus, models.SET_NULL, db_column='status_id', related_name='client_status',
                               null=True)
    # city = models.ForeignKey(City, models.CASCADE, related_name='client_city', db_column='cities_light_city_id')
    city = models.CharField(max_length=150, null=True)
    state = models.CharField(max_length=150, null=True)
    country = models.CharField(max_length=150, null=True)
    main_branch = models.ForeignKey('self', null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_branch',
                                    db_column='sales_force_id', null=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    @property
    def getParsedQuery(self):
        txt = ''
        for field in self._meta.fields:
            txt += '[' + field.name + ':' + str(getattr(self, str(field.name))) + ']'
        return txt

    @property
    def getAvatar(self):
        if self.avatar:
            return self.avatar.url
        return settings.STATIC_URL + 'img/default_avatar_male.jpg'

    @property
    def getObjectAsJson(self):
        json = '{'
        for field in self._meta.fields:
            json + field.name + ":" + str(getattr(self, str(field.name))) + ','
        json += '}'
        return json

    class Meta:
        managed = MANAGED
        db_table = 'client'
        unique_together = ['name', 'corporate', 'phone']


class Tags(models.Model):
    name = models.CharField(max_length=150, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id', null=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_tags', db_column='corp_id')

    def __str__(self):
        return self.name

    class Meta:
        managed = MANAGED
        db_table = 'tags'


class ClientTags(models.Model):
    client_tags = models.ForeignKey(Client, models.CASCADE, related_name='client_tags', db_column='branch_id')
    tags = models.ForeignKey(Tags, models.CASCADE, related_name='client_tags', db_column='tag_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id', null=True)

    class Meta:
        managed = MANAGED
        db_table = 'branch_tags'


class SalesForceSchedual(models.Model):
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_schedual',
                                    db_column='sales_force_id')
    branch = models.ForeignKey(Client, models.CASCADE, related_name='branch_schedual', db_column='branch_id')
    schedual_date = models.DateField(null=False)
    schedual_time = models.TimeField(null=False)
    notes = models.TextField(null=True)
    is_visit = models.BooleanField(default=True)

    @property
    def getParsedQuery(self):
        txt = ''
        for field in self._meta.fields:
            txt += '[' + field.name + ':' + str(getattr(self, str(field.name))) + ']'
        return txt

    @property
    def getObjectAsJson(self):
        json = '{'
        for field in self._meta.fields:
            print field.name
            json += field.name + ":" + str(getattr(self, str(field.name))) + ','
        json += '}'
        return json

    class Meta:
        managed = MANAGED
        db_table = 'schedual'


class ProductGroup(models.Model):
    name = models.CharField(max_length=150, null=False)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_product_group', db_column='corp_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def getParsedQuery(self):
        txt = ''
        for field in self._meta.fields:
            txt += '[' + field.name + ':' + str(getattr(self, str(field.name))) + ']'
        return txt

    class Meta:
        managed = MANAGED
        db_table = 'product_group'


class ProductUnit(models.Model):
    name = models.CharField(max_length=150, null=False)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_product_unit', db_column='corp_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = MANAGED
        db_table = 'product_unit'


class Product(models.Model):
    name = models.CharField(max_length=150, null=False)
    ean_code = models.CharField(max_length=150)
    default_price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    product = models.ForeignKey(ProductGroup, models.CASCADE, related_name='group_products',
                                db_column='product_group_id')
    unit = models.ForeignKey(ProductUnit, models.CASCADE, related_name='product_unit', db_column='unit_id', null=True)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_product', db_column='corp_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=settings.PRODUCT_DIR)
    slug = models.SlugField()

    @property
    def getParsedQuery(self):
        txt = ''
        for field in self._meta.fields:
            txt += '[' + field.name + ':' + str(getattr(self, str(field.name))) + ']'
        return txt

    class Meta:
        managed = MANAGED
        db_table = 'product'
        unique_together = ['name', 'corporate']


class ProductTags(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name='product_tag', db_column='product_id')
    tag = models.ForeignKey(Tags, models.CASCADE, related_name='tag_product', db_column='tag_id')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'product_tag'


class PriceList(models.Model):
    name = models.CharField(max_length=150, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = MANAGED
        db_table = 'price_list'


class ProductPriceList(models.Model):
    price_list = models.ForeignKey(PriceList, models.CASCADE, related_name='price_list_product',
                                   db_column='price_list_id')
    product = models.ForeignKey(Product, models.CASCADE, related_name='product_price_list', db_column='product_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = MANAGED
        db_table = 'product_price_list'


class SystemSettings(models.Model):
    mileage_tracking = models.CharField(max_length=20, null=False)
    add_place_via_mobile = models.BooleanField(default=True)
    edit_place_via_mobile = models.BooleanField(default=True)
    assign_sales_force_via_mobile = models.BooleanField(default=True)
    show_inactive_rep_in_webapp = models.BooleanField(default=True)
    see_other_rep_activity = models.BooleanField(default=True)
    upload_image_via_mobile = models.BooleanField(default=True)
    manage_schedual = models.BooleanField(default=True)
    elec_sign_in_order = models.BooleanField(default=False)
    elec_sign_in_form = models.BooleanField(default=False)
    send_email_via_mobile = models.BooleanField(default=False)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_settings', db_column='corp_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')

    class Meta:
        managed = MANAGED
        db_table = 'system_settings'


class BillBoard(models.Model):
    subject = models.CharField(max_length=150, null=False)
    body = models.TextField(null=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=False)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_billboeard', db_column='corp_id')

    @property
    def getParsedQuery(self):
        txt = ''
        for field in self._meta.fields:
            txt += '[' + field.name + ':' + str(getattr(self, str(field.name))) + ']'
        return txt

    class Meta:
        managed = MANAGED
        db_table = 'billboard'
        unique_together = ['subject', 'corporate']


class Messages(models.Model):
    reciept = models.ForeignKey(User, models.CASCADE, related_name='reciept_user', db_column='reciept_auth_user_id')
    sender = models.ForeignKey(User, models.CASCADE, related_name='sender_user', db_column='sender_auth_user_id')
    body = models.TextField(null=False)
    message_thread = models.ForeignKey('self', null=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'message'


class Visits(models.Model):
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_visits',
                                    db_column='sales_force_id')
    branch = models.ForeignKey(Client, models.CASCADE, related_name='branch_visits', db_column='branch_id')
    visit_date = models.DateField(null=True)
    notes = models.TextField(null=True)
    schedualed = models.BooleanField(default=True)
    schedual = models.ForeignKey(SalesForceSchedual, models.CASCADE, related_name='visit_schedual',
                                 db_column='schedual_id', null=True)
    created_date = models.DateTimeField(default=timezone.now)

    @property
    def getParsedQuery(self):
        txt = ''
        for field in self._meta.fields:
            txt += '[' + field.name + ':' + str(getattr(self, str(field.name))) + ']'
        return txt

    class Meta:
        managed = MANAGED
        db_table = 'visits'


class Orders(models.Model):
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_orders',
                                    db_column='sales_force_id')
    branch = models.ForeignKey(Client, models.CASCADE, related_name='branch_order', db_column='branch_id')
    order_date = models.DateTimeField(null=False)
    total = models.FloatField()
    sub_total = models.FloatField()
    discount = models.DecimalField(max_digits=9, decimal_places=3)
    created_form_visit = models.ForeignKey(Visits, models.CASCADE, related_name='order_visits', db_column='visit_id',
                                           null=True)
    order_number = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    notes = models.TextField(null=True)
    created_date = models.DateTimeField(default=timezone.now)

    @property
    def getParsedQuery(self):
        txt = ''
        for field in self._meta.fields:
            txt += '[' + field.name + ':' + str(getattr(self, str(field.name))) + ']'
        return txt

    class Meta:
        managed = MANAGED
        db_table = 'order'


class OrderLine(models.Model):
    order = models.ForeignKey(Orders, models.CASCADE, related_name='order_lines', db_column='order_id')
    product = models.ForeignKey(Product, models.DO_NOTHING, related_name='order_product', db_column='product_id')
    price = models.FloatField(null=False)
    quantity = models.IntegerField()

    class Meta:
        managed = MANAGED
        db_table = 'order_line'


class SalesForceTimeLine(models.Model):
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_time_line',
                                    db_column='sales_force_id')
    time_line_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True)
    km = models.DecimalField(max_digits=9, decimal_places=3)
    hours = models.DecimalField(max_digits=9, decimal_places=3)

    class Meta:
        managed = MANAGED
        db_table = 'sales_force_timeline'


class SalesForceCheckInOut(models.Model):
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_check_in',
                                    db_column='sales_force_id')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_date = models.DateField(null=True)
    check_out_time = models.TimeField(null=True)
    check_in_address = models.TextField()
    check_out_address = models.TextField()
    branch = models.ForeignKey(Client, models.CASCADE, related_name='branch_check_in_out', db_column='branch_id',
                               null=True)
    visit = models.ForeignKey(Visits, models.CASCADE, related_name='visit_check_in_out', db_column='visit_id',
                              null=True)

    @property
    def getTimeDiff(self):
        from datetime import datetime
        tdelta = 0
        FMT = '%H:%M:%S'
        if self.check_out_time and self.check_in_time:
            tdelta = datetime.strptime(str(self.check_out_time), FMT) - datetime.strptime(str(self.check_in_time), FMT)

        return tdelta

    @property
    def getDelay(self):
        from datetime import datetime
        FMT = '%H:%M:%S'
        visit_date = self.visit.created_date
        schedul_date = self.visit.schedual.schedual_time
        tdelta = datetime.strptime(str(visit_date.time().strftime(FMT)), FMT) - datetime.strptime(str(schedul_date),
                                                                                                  FMT)
        return tdelta
    
    @property
    def get_sec(self):
        h, m, s = str(self.getDelay).split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)


    @property
    def getDistance(self):
        client = self.branch
        lat_a = radians(self.latitude)
        lat_b = radians(client.latitude)
        long_diff = radians(self.longitude - client.longitude)
        distance = (sin(lat_a) * sin(lat_b) +
                    cos(lat_a) * cos(lat_b) * cos(long_diff))

        return float("{:.2f}".format(degrees(acos(distance)) * 69.09))

    class Meta:
        managed = MANAGED
        db_table = 'sales_force_check_in_out'


class SalesForceTrack(models.Model):
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_tracking',
                                    db_column='sales_force_id')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.sales_force.name + '-- Corp ' + self.sales_force.corp_id.corporate_name

    class Meta:
        managed = MANAGED
        db_table = 'sales_force_tracking'
        ordering = ['-created_date']


class Forms(models.Model):
    form_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_forms', db_column='corp_id')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)

    @property
    def getParsedQuery(self):
        txt = ''
        for field in self._meta.fields:
            txt += '[' + field.name + ']:' + str(getattr(self, str(field.name)))
        return txt

    class Meta:
        managed = MANAGED
        db_table = 'forms'
        unique_together = ['form_name', 'corporate']


class FormQuestions(models.Model):
    form = models.ForeignKey(Forms, models.CASCADE, related_name='form_questions', db_column='form_id')
    question = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'forms_questions'


class QuestionAnswer(models.Model):
    question = models.ForeignKey(FormQuestions, models.CASCADE, related_name='questions_answer',
                                 db_column='question_id')
    answer = models.TextField(null=False)
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_question',
                                    db_column='sales_force_id')
    branch = models.ForeignKey(Client, models.CASCADE, related_name='branch_answer', db_column='branch_id')
    visit = models.ForeignKey(Visits, models.CASCADE, related_name='visit_form', db_column='visit_id')

    class Meta:
        managed = MANAGED
        db_table = 'question_answer'


class AuditRetails(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=100)
    action_type = models.CharField(max_length=100)
    details = models.TextField(null=False)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_audit_retails', db_column='corp_id')

    class Meta:
        managed = MANAGED
        db_table = 'audit_retails'
