from django.db import models
from teachers.models import Teacher


# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=250)
    teacher = models.OneToOneField(Teacher, models.DO_NOTHING, db_column='teacher_ma')

    class Meta:
        managed = False
        db_table = 'user'
