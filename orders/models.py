from __future__ import unicode_literals

import uuid as uuid

from django.db import models
from decimal import Decimal
from django.conf import settings

# every Django model fields can be customized by re-use parameter under
# simple dictionary format 
AMOUNT_MONEY = {
                'max_digits': 25, 'decimal_places': 2, 
                'default': Decimal('0.00')
               }

class CommonInfo(models.Model):
    """
    Abstract models contains mandatory fields on each models.
    Every class can have these fields by instantiate from this class.
    """
    remarks = models.TextField(blank=True, verbose_name='Keterangan Tambahan')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Waktu Dibuat')
    modified = models.DateTimeField(auto_now=True, verbose_name='Waktu diedit')
    status = models.BooleanField(default=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    # flag for update, delete, sync and coming from cloud
    is_delete = models.BooleanField(default=False, verbose_name='Soft Delete')

    class Meta:
        abstract = True


class ODOrder(CommonInfo):
    """
    Order details contain name, phone and amount of total price order 
    """
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    price = models.DecimalField(**AMOUNT_MONEY)

    def __unicode__(self):
        return '{}'.format(self.user.username)

    class Meta:
        verbose_name_plural = "Customer"



class Vehicle(models.Model):
    """
    Vehicles contai8n name, driver, number and capacity
    """

    number = models.CharField(max_length=10, unique=True, verbose_name="Nomer Kendaraan")
    name = models.CharField(max_length=30, verbose_name="Nama Kendaraan")
    driver = models.CharField(max_length=40, verbose_name="Sopir")
    capacity = models.PositiveIntegerField(verbose_name="Kapasitas Muatan")
    # need package Pillow (i used in version 3.3.0), i put in requirements.txt
    photo = models.ImageField(upload_to='vehicles/%Y/%m/%d', blank=True, 
        verbose_name="Foto Kendaraan")

    def __unicode__(self):
        return self.number





