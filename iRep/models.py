# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cities_light.models import City, Region, Country
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)

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
    corp_id = models.ForeignKey(Corporate, models.CASCADE, related_name='sales_force_corp', db_column='corp_id')
    user_pin = models.CharField(max_length=150, null=False)
    password_pin = models.CharField(max_length=150, null=False)
    notes = models.TextField()
    last_activity = models.DateTimeField()
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = MANAGED
        db_table = 'sales_force'


class Client(models.Model):
    avatar = models.ImageField(upload_to=settings.AVATAR_DIR, null=True)
    name = models.CharField(max_length=150, null=False)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corporate_client', db_column='corp_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)

    class Meta:
        managed = MANAGED
        db_table = 'client'


class Branches(models.Model):
    avatar = models.ImageField(upload_to=settings.AVATAR_DIR, null=True)
    name = models.CharField(max_length=150, null=False)
    address_txt = models.CharField(max_length=200, null=False)
    city = models.ForeignKey(City, models.CASCADE, related_name='client_city', db_column='cities_light_city_id')
    zipcode = models.IntegerField()
    contact_name = models.CharField(max_length=150)
    contact_title = models.CharField(max_length=100)
    website = models.URLField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cell_phone = models.CharField(max_length=20)
    notes = models.TextField()
    status = models.ForeignKey(SalesFunnelStatus, models.SET_NULL, db_column='status_id', related_name='client_status',
                               null=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = MANAGED
        db_table = 'branches'


class Tags(models.Model):
    name = models.CharField(max_length=150, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_tags', db_column='corp_id')

    class Meta:
        managed = MANAGED
        db_table = 'tags'


class SalesForceBranches(models.Model):
    branch = models.ForeignKey(Branches, models.CASCADE, related_name='client_branch', db_column='branch_id')
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_branch',
                                    db_column='sales_force_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')

    class Meta:
        managed = MANAGED
        db_table = 'sales_force_branches'


class BranchesTags(models.Model):
    branch = models.ForeignKey(Branches, models.CASCADE, related_name='branch_tags', db_column='branch_id')
    tags = models.ForeignKey(Tags, models.CASCADE, related_name='tags', db_column='tag_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')

    class Meta:
        managed = MANAGED
        db_table = 'branch_tags'


class SalesForceSchedual(models.Model):
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_schedual',
                                    db_column='sales_force_id')
    branch = models.ForeignKey(Branches, models.CASCADE, related_name='branch_schedual', db_column='branch_id')
    schedual_date = models.DateField(null=False)
    schedual_time = models.TimeField(null=False)
    notes = models.TextField()

    class Meta:
        managed = MANAGED
        db_table = 'schedual'


class ProductGroup(models.Model):
    name = models.CharField(max_length=150, null=False)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_product_group', db_column='corp_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = MANAGED
        db_table = 'product_group'


class ProductUnit(models.Model):
    name = models.CharField(max_length=150, null=False)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='corp_product_unit', db_column='corp_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = MANAGED
        db_table = 'product_unit'


class Product(models.Model):
    name = models.CharField(max_length=150, null=False)
    ean_code = models.CharField(max_length=150)
    default_price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    product_group = models.ForeignKey(ProductGroup, models.CASCADE, related_name='product_group',
                                      db_column='product_group_id')
    unit = models.ForeignKey(ProductUnit, models.CASCADE, related_name='product_unit', db_column='unit_id')
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = MANAGED
        db_table = 'product'


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

    class Meta:
        managed = MANAGED
        db_table = 'billboard'


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
    branch = models.ForeignKey(Branches, models.CASCADE, related_name='branch_visits', db_column='branch_id')
    visit_date = models.DateTimeField(null=False)
    notes = models.TextField()
    schedualed = models.BooleanField(default=True)
    schedual = models.ForeignKey(SalesForceSchedual, models.CASCADE, related_name='visit_schedual',
                                 db_column='schedual_id', null=True)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = MANAGED
        db_table = 'visits'


class Orders(models.Model):
    sales_force = models.ForeignKey(SalesForce, models.CASCADE, related_name='sales_force_orders',
                                    db_column='sales_force_id')
    branch = models.ForeignKey(Branches, models.CASCADE, related_name='branch_order', db_column='branch_id')
    order_date = models.DateTimeField(null=False)
    total = models.FloatField()
    created_form_visit = models.ForeignKey(Visits, models.CASCADE, related_name='order_visits', db_column='visit_id',
                                           null=True)
    notes = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

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
