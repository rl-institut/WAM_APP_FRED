from django.db import models


class CsvRow(models.Model):
    time = models.CharField(max_length=30)
    val = models.CharField(max_length=30)

class CsvName(models.Model):
    fname = models.CharField(max_length=100)