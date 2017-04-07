# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cities_light.admin import City
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
    created_by = models.ForeignKey('iRep.User', on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)

    class Meta:
        managed = MANAGED
        db_table = 'corporates'
        verbose_name_plural = _('Corporates')
        ordering = ['-created_date']


class Clients(models.Model):
    avatar = models.ImageField(upload_to='', null=True)
    name =models.CharField(max_length=150, null=False)
    address_txt = models.CharField(max_length=200, null=False)
    city = models.ForeignKey(City, default=None, related_name='client_city', db_column='cities_light_city_id')
    zipcode = models.IntegerField()
    contact_name = models.CharField(max_length=150)
    contact_title = models.CharField(max_length=100)
    website = models.URLField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cell_phone = models.CharField(max_length=20)
    notes = models.TextField()
    status = models.ForeignKey()
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('iRep.User', on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)

    def __unicode__(self):
        return self.name

    class Meta:
        managed = MANAGED
        db_table = 'clients'


class ClientStatus(models.Model):
    status_name = models.CharField(max_length=150)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('iRep.User', on_delete=models.CASCADE, db_column='auth_user_id')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(db_index=True)

    def __unicode__(self):
        return self.status_name

    class Meta:
        managed = MANAGED
        db_table = 'client_status'
        ordering = ['-created_date']


class User(AbstractBaseUser, PermissionsMixin):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.

        Username and password are required. Other fields are optional.
        """
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    corperate = models.ForeignKey(Corporate, models.CASCADE, db_column='corperate_id', related_name='user_corp',
                                  null=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
