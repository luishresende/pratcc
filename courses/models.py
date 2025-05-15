from django.db import models
from campus.models import Campus


class Course(models.Model):
    campus = models.ForeignKey(Campus, models.DO_NOTHING)
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'course'
