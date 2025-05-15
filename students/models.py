from django.db import models
from courses.models import Course
from teachers.models import Teacher


# Create your models here.
class Student(models.Model):
    ra = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=120)
    course = models.ForeignKey(Course, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'student'
