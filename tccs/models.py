from django.db import models
from students.models import Student
from teachers.models import Teacher


class TccWork(models.Model):
    tcc_id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    semester = models.IntegerField()
    tcc_num = models.IntegerField()
    student_ra = models.ForeignKey(Student, models.DO_NOTHING, db_column='student_ra', related_name='tccworks')
    teacher_advisor_ma = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacher_advisor_ma')
    teacher_cosupervisor_ma = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='teacher_cosupervisor_ma', related_name='tccwork_teacher_cosupervisor_ma_set', blank=True, null=True)
    title = models.CharField(max_length=100)

    class Meta:
        # constraints = [
        #     models.UniqueConstraint(fields=['student_ra', 'year', 'semester'], name='unique_tcc_per_student_per_period')
        # ]
        managed = False
        db_table = 'tcc_work'


class TccCommittee(models.Model):
    tccw = models.OneToOneField(TccWork, models.DO_NOTHING, primary_key=True)
    full_member_1_ma = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='full_member_1_ma')
    full_member_2_ma = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='full_member_2_ma', related_name='tcccommittee_full_member_2_ma_set')
    alternate_member_ma = models.ForeignKey(Teacher, models.DO_NOTHING, db_column='alternate_member_ma', related_name='tcccommittee_alternate_member_ma_set')
    defense_date = models.DateTimeField()
    defense_location = models.CharField(max_length=120)
    authorization_letter_submitted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'tcc_committee'


class TccDocuments(models.Model):
    tccw = models.OneToOneField(TccWork, models.DO_NOTHING, primary_key=True)
    fm1_evaluation_form = models.IntegerField(default=0)
    fm2_evaluation_form = models.IntegerField(default=0)
    fm3_evaluation_form = models.IntegerField(default=0)
    approvation_term = models.IntegerField(default=0)
    end_monograph = models.IntegerField(default=0)
    end_monograph_in_lib = models.IntegerField(default=0)
    recorded_data = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'tcc_documents'
