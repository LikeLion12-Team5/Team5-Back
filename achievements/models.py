from django.db import models

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    explain = models.CharField(max_length=200)
