# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Campus(models.Model):
    university_acronym = models.ForeignKey('University', models.DO_NOTHING, db_column='university_acronym')
    city = models.ForeignKey('City', models.DO_NOTHING)
    name = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'campus'


class City(models.Model):
    state_acronym = models.ForeignKey('State', models.DO_NOTHING, db_column='state_acronym')
    name = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'city'


class Course(models.Model):
    campus = models.ForeignKey(Campus, models.DO_NOTHING)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'course'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class State(models.Model):
    acronym = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'state'


class Student(models.Model):
    ra = models.CharField(primary_key=True, max_length=8)
    course = models.ForeignKey(Course, models.DO_NOTHING)
    name = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'student'


class TccCommittee(models.Model):
    tccw = models.OneToOneField('TccWork', models.DO_NOTHING, primary_key=True)
    full_member_1_ma = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='full_member_1_ma')
    fm1_evaluation_form = models.IntegerField(blank=True, null=True)
    full_member_2_ma = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='full_member_2_ma', related_name='tcccommittee_full_member_2_ma_set')
    fm2_evaluation_form = models.IntegerField(blank=True, null=True)
    alternate_member_ma = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='alternate_member_ma', related_name='tcccommittee_alternate_member_ma_set')
    am_evaluation_form = models.IntegerField(blank=True, null=True)
    defense_date = models.DateTimeField()
    defense_location = models.CharField(max_length=120)
    approvation_term = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tcc_committee'


class TccMonograph(models.Model):
    tccw = models.OneToOneField('TccWork', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'tcc_monograph'


class TccWork(models.Model):
    tcc_id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    semester = models.IntegerField()
    tcc_num = models.IntegerField()
    student_ra = models.ForeignKey(Student, models.DO_NOTHING, db_column='student_ra')
    teacher_advisor_ma = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacher_advisor_ma')
    teacher_cosupervisor_ma = models.ForeignKey('Teacher', models.DO_NOTHING, db_column='teacher_cosupervisor_ma', related_name='tccwork_teacher_cosupervisor_ma_set', blank=True, null=True)
    title = models.CharField(max_length=100)
    authorization_letter_submitted = models.IntegerField()
    end_monograph = models.IntegerField()
    end_monograph_in_lib = models.IntegerField(blank=True, null=True)
    recorded_data = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tcc_work'


class Teacher(models.Model):
    teacher_ma = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=120)
    course = models.ForeignKey(Course, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teacher'


class University(models.Model):
    acronym = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'university'


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=250)
    teacher_ma = models.OneToOneField(Teacher, models.DO_NOTHING, db_column='teacher_ma')

    class Meta:
        managed = False
        db_table = 'user'
