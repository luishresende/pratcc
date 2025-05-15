from django.db import models
from universities.models import University


# Create your models here.
class State(models.Model):
    acronym = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'state'


    def __str__(self):
        return f"{self.name} ({self.acronym})"


class City(models.Model):
    state_acronym = models.ForeignKey('State', models.DO_NOTHING, db_column='state_acronym')
    name = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'city'


# Create your models here.
class Campus(models.Model):
    university = models.ForeignKey(
        'universities.University',
        models.DO_NOTHING,
        to_field='acronym',
        db_column='university_acronym'
    )
    city = models.ForeignKey('City', models.DO_NOTHING)
    name = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'campus'