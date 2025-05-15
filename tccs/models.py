from django.db import models
from students.models import Student
from teachers.models import Teacher


class TccCommittee(models.Model):
    tccw = models.OneToOneField('TccWork', models.DO_NOTHING, primary_key=True)
    full_member_1_ma = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='full_member_1_ma')
    fm1_evaluation_form = models.IntegerField(blank=True, null=True)
    full_member_2_ma = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='full_member_2_ma', related_name='tcccommittee_full_member_2_ma_set')
    fm2_evaluation_form = models.IntegerField(blank=True, null=True)
    alternate_member_ma = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='alternate_member_ma', related_name='tcccommittee_alternate_member_ma_set')
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
    student_ra = models.ForeignKey(
        Student,
        models.DO_NOTHING,
        db_column='student_ra',
        related_name='tccworks'  # ← aqui
    )
    teacher_advisor_ma = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacher_advisor_ma')
    teacher_cosupervisor_ma = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacher_cosupervisor_ma', related_name='tccwork_teacher_cosupervisor_ma_set', blank=True, null=True)
    title = models.CharField(max_length=100)
    authorization_letter_submitted = models.IntegerField()
    end_monograph = models.IntegerField()
    end_monograph_in_lib = models.IntegerField(blank=True, null=True)
    recorded_data = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tcc_work'