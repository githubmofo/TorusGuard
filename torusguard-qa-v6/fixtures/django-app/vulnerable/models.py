from django.db import models

class Invoice(models.Model):
    title = models.CharField(max_length=200)
    tenant_id = models.CharField(max_length=50)
