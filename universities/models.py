from django.db import models

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=150)
    acronym = models.CharField(max_length=10, primary_key=True)

    class Meta:
        managed = False
        db_table = 'university'

    def __str__(self):
        return self.name