from django.db import models

class Spending(models.Model):
    value    = models.DecimalField()
    source   = models.UrlField()
    name     = models.CharField()
    currency = models.ForeignKey()