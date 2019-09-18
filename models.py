from django.db import models


class CsvRow(models.Model):
    time = models.CharField(max_length=30)
    val = models.CharField(max_length=30)
    height = models.CharField(max_length=30, default='none')


class CsvParam(models.Model):
    fname = models.CharField(max_length=100)
    height = models.CharField(max_length=30, default='none')
