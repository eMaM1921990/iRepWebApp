__author__ = 'eMaM'

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from iRep.models import SalesForce, AuditRetails, Client, SalesForceSchedual, ProductGroup, Product, BillBoard, Visits, \
    Orders, Forms


@receiver(post_save, sender=SalesForce)
def salesForceCreatedOrUpdated(sender, instance, created, **kwargs):
    if created:
        AuditRetails(created_by=instance.created_by,
                     action_type='Insert',
                     details=instance.getParsedQuery,corporate=instance.corp_id).save()

    else:
        AuditRetails(created_by=instance.created_by,
                     action_type='Update',
                     details=instance.getParsedQuery,corporate=instance.corp_id).save()


@receiver(pre_delete, sender=SalesForce)
def salesForceDeleted(sender, instance, **kwargs):
    AuditRetails(created_by=instance.created_by,
                 action_type='Delete',
                 details=instance.getParsedQuery,corporate=instance.corp_id).save()


@receiver(post_save, sender=Client)
def clientCreatedOrUpdated(sender, instance, created, **kwargs):
    if created:
        AuditRetails(created_by=instance.created_by,
                     action_type='Insert',
                     details=instance.getParsedQuery,corporate=instance.corporate).save()
    else:
        AuditRetails(created_by=instance.created_by,
                     action_type='Update',
                     details=instance.getParsedQuery,corporate=instance.corporate).save()


@receiver(pre_delete, sender=Client)
def clientDeleted(sender, instance, **kwargs):
    AuditRetails(created_by=instance.created_by,
                 action_type='Delete',
                 details=instance.getParsedQuery,corporate=instance.corporate).save()


@receiver(post_save, sender=SalesForceSchedual)
def salesForceScedualCreatedOrUpdated(sender, instance, created, **kwargs):
    if created:
        AuditRetails(created_by='',
                     action_type='Add schedual',
                     details=instance.getParsedQuery,corporate=instance.sales_force.corp_id).save()
    else:
        AuditRetails(created_by='',
                     action_type='Update schedual',
                     details=instance.getParsedQuery,corporate=instance.sales_force.corp_id).save()


@receiver(pre_delete, sender=SalesForceSchedual)
def salesForceScedualDeleted(sender, instance, **kwargs):
    AuditRetails(created_by='',
                 action_type='Delete schedual',
                 details=instance.getParsedQuery,corporate=instance.sales_force.corp_id).save()


@receiver(post_save, sender=ProductGroup)
def productGroupCreatedOrUpdated(sender, instance, created, **kwargs):
    if created:
        AuditRetails(created_by=instance.created_by,
                     action_type='Add ',
                     details=instance.getParsedQuery,corporate=instance.corporate).save()
    else:
        AuditRetails(created_by=instance.created_by,
                     action_type='Update ',
                     details=instance.getParsedQuery,corporate=instance.corporate).save()


@receiver(pre_delete, sender=ProductGroup)
def productGroupDeleted(sender, instance, **kwargs):
    AuditRetails(created_by=instance.created_by,
                 action_type='Delete ',
                 details=instance.getParsedQuery,corporate=instance.corporate).save()


@receiver(post_save, sender=Product)
def productCreatedOrUpdated(sender, instance, created, **kwargs):
    if created:
        AuditRetails(created_by=instance.created_by,
                     action_type='Add ',
                     details=instance.getParsedQuery,corporate=instance.corporate).save()
    else:
        AuditRetails(created_by=instance.created_by,
                     action_type='Update ',
                     details=instance.getParsedQuery,corporate=instance.corporate).save()


@receiver(pre_delete, sender=Product)
def productDeleted(sender, instance, **kwargs):
    AuditRetails(created_by=instance.created_by,
                 action_type='Delete ',
                 details=instance.getParsedQuery,corporate=instance.corporate).save()


@receiver(post_save, sender=BillBoard)
def billBoardCreatedOrUpdated(sender, instance, created, **kwargs):
    if created:
        AuditRetails(created_by=instance.created_by,
                     action_type='Add ',
                     details=instance.getParsedQuery,corporate=instance.corporate).save()
    else:
        AuditRetails(created_by=instance.created_by,
                     action_type='Update ',
                     details=instance.getParsedQuery,corporate=instance.corporate).save()


@receiver(pre_delete, sender=BillBoard)
def billBoardDeleted(sender, instance, **kwargs):
    AuditRetails(created_by=instance.created_by,
                 action_type='Delete ',
                 details=instance.getParsedQuery,corporate=instance.corporate).save()


@receiver(post_save, sender=Visits)
def visitCreatedOrUpdated(sender, instance, created, **kwargs):
    if created:
        AuditRetails(created_by=instance.created_by,
                     action_type='Add visit',
                     details=instance.getParsedQuery,corporate=instance.sales_force.corp_id).save()
    else:
        AuditRetails(created_by=instance.created_by,
                     action_type='Update visit',
                     details=instance.getParsedQuery,corporate=instance.sales_force.corp_id).save()


@receiver(pre_delete, sender=Visits)
def visitDeleted(sender, instance, **kwargs):
    AuditRetails(created_by=instance.created_by,
                 action_type='Delete visit',
                 details=instance.getParsedQuery,corporate=instance.sales_force.corp_id).save()


@receiver(post_save, sender=Orders)
def orderCreatedOrUpdated(sender, instance, created, **kwargs):
    if created:
        AuditRetails(created_by=instance.created_by,
                     action_type='Add Order',
                     details=instance.getParsedQuery,corporate=instance.sales_force.corp_id).save()
    else:
        AuditRetails(created_by=instance.created_by,
                     action_type='Update Order',
                     details=instance.getParsedQuery,corporate=instance.sales_force.corp_id).save()


@receiver(pre_delete, sender=Orders)
def orderDeleted(sender, instance, **kwargs):
    AuditRetails(created_by=instance.created_by,
                 action_type='Delete Order',
                 details=instance.getParsedQuery,corporate=instance.sales_force.corp_id).save()


@receiver(post_save, sender=Forms)
def formsCreatedOrUpdated(sender, instance, created, **kwargs):
    if created:
        AuditRetails(created_by=instance.created_by,
                     action_type='Add Forms',
                     details=instance.getParsedQuery,corporate=instance.corporate).save()
    else:
        AuditRetails(created_by=instance.created_by,
                     action_type='Update Forms',
                     details=instance.getParsedQuery,corporate=instance.corporate).save()


@receiver(pre_delete, sender=Forms)
def formsDeleted(sender, instance, **kwargs):
    AuditRetails(created_by=instance.created_by,
                 action_type='Delete Forms',
                 details=instance.getParsedQuery,corporate=instance.corporate).save()
