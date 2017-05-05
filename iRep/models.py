# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cities_light.models import City, Region, Country
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from managers.UserManager import UserManager
from django.utils import six, timezone

MANAGED = True


# Create your models here.
class UserProfile(models.Model):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    user_type = models.IntegerField(default=0)
    corporate = models.ForeignKey(Corporate, models.CASCADE, related_name='user_profile_corp', db_column='corp_id')

    class Meta:
        managed = MANAGED
        db_table = 'user_profile'


class Corporate(models.Model):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
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


class Client(models.Model):
    avatar = models.ImageField(upload_to='', null=True)
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
    avatar = models.ImageField(upload_to='', null=True)
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


class SalesForce(models.Model):
    avatar = models.ImageField(upload_to='')
    name = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    email = models.EmailField(null=False)
    profile_language = models.ForeignKey(AppLanguage, models.CASCADE, related_name='profile_lang',
                                         db_column='profile_lang_id')
    login_company = models.ForeignKey(Corporate, models.CASCADE, related_name='sales_force_corp', db_column='corp_id')
    login_user_id = models.CharField(max_length=150, null=False)
    login_password = models.CharField(max_length=150, null=False)
    notes = models.TextField()
    last_activity = models.DateTimeField()
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = MANAGED
        db_table = 'sales_force'


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
    default_price = models.DecimalField()
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
