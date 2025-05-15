from django.db import models
from courses.models import Course


# Create your models here.
class Teacher(models.Model):
    ma = models.CharField(primary_key=True, max_length=8, db_column='teacher_ma')
    name = models.CharField(max_length=120)
    course = models.ForeignKey(Course, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teacher'