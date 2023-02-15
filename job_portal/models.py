import uuid
from django.db import models
from django.utils import timezone
from authentication.models import User
from job_portal.utils.job_status import JOB_STATUS_CHOICE


class JobDetail(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False)
    job_title = models.CharField(max_length=2000)
    company_name = models.CharField(max_length=2000,null=True,blank=True)
    job_source = models.CharField(max_length=2000)
    job_type = models.CharField(max_length=2000,null=True,blank=True)
    address = models.CharField(max_length=2000)
    job_description = models.TextField(null=True,blank=True)
    tech_keywords = models.TextField(null=True,blank=True)
    job_posted_date = models.DateTimeField(null=True,blank=True)
    job_source_url = models.CharField(max_length=2000,null=True,blank=True)
    job_status = models.IntegerField(default=0, choices=JOB_STATUS_CHOICE)

    class Meta:
        db_table = "job_detail"
        unique_together = (('company_name','job_title','job_source_url'),)
        ordering = ['-job_posted_date']
        # indexes = [models.Index(fields=['company_name','job_source','tech_keywords','job_posted_date'])]

    def __str__(self):
        return self.job_title


class AppliedJobStatus(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    job = models.OneToOneField(
        JobDetail,
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    applied_by = models.ForeignKey(
        User,
        verbose_name='applied by',
        on_delete=models.CASCADE,
        blank=True, null=False)
    applied_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "applied_job_status"
        ordering = ["id"]

    def __str__(self):
        return str(self.id.uuid4())
