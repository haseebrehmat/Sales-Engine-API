import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from authentication.models import User, Team
from authentication.models.company import Company
from job_portal.utils.job_status import JOB_STATUS_CHOICE
from pseudos.models import Verticals
from settings.utils.model_fields import TimeStamped


class JobDetail(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    job_title = models.CharField(max_length=2000)
    company_name = models.CharField(max_length=2000, null=True, blank=True)
    job_source = models.CharField(max_length=2000)
    job_type = models.CharField(max_length=2000, null=True, blank=True)
    address = models.CharField(max_length=2000)
    job_description = models.TextField(null=True, blank=True)
    job_description_tags = models.TextField(null=True, blank=True)
    tech_keywords = models.TextField(null=True, blank=True)
    job_posted_date = models.DateTimeField(null=True, blank=True)
    job_source_url = models.CharField(max_length=2000, null=True, blank=True)
    block = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=False)
    job_applied = models.CharField(max_length=300, default="not applied")
    status = models.CharField(blank=True, null=True, max_length=50)
    salary_max = models.CharField(max_length=50, blank=True, null=True)
    salary_min = models.CharField(max_length=50, blank=True, null=True)
    salary_format = models.CharField(max_length=50, blank=True, null=True)
    estimated_salary = models.CharField(blank=True, null=True, max_length=100)
    expired_at = models.DateTimeField(max_length=150, blank=True, null=True)
    job_role = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        default_permissions = ()
        db_table = "job_detail"
        unique_together = (('company_name', 'job_title', 'job_applied'),)
        ordering = ['-job_posted_date']
        indexes = [models.Index(
            fields=['company_name', 'job_source', 'tech_keywords', 'job_posted_date'])]
        index_together = ['company_name', 'job_title']

    def __str__(self):
        return self.job_title


class JobArchive(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    job_title = models.CharField(max_length=2000)
    company_name = models.CharField(max_length=2000, null=True, blank=True)
    job_source = models.CharField(max_length=2000)
    job_type = models.CharField(max_length=2000, null=True, blank=True)
    address = models.CharField(max_length=2000)
    job_description = models.TextField(null=True, blank=True)
    tech_keywords = models.TextField(null=True, blank=True)
    job_posted_date = models.DateTimeField(null=True, blank=True)
    job_source_url = models.CharField(max_length=2000, null=True, blank=True)
    block = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=False)

    class Meta:
        default_permissions = ()
        db_table = "job_archive"
        ordering = ['-job_posted_date']
        indexes = [models.Index(
            fields=['job_source', 'tech_keywords', 'job_posted_date', 'created_at'])]
        index_together = ['company_name', 'job_title']

    def __str__(self):
        return self.job_title


class AppliedJobStatus(models.Model):
    vertical = models.ForeignKey(
        Verticals, on_delete=models.SET_NULL, blank=True, null=True)
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, blank=True, null=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    job = models.ForeignKey(
        'JobDetail',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    applied_by = models.ForeignKey(
        User,
        verbose_name='applied by',
        on_delete=models.CASCADE,
        blank=True, null=False)
    applied_date = models.DateTimeField(default=timezone.now)
    job_status = models.IntegerField(default=0, choices=JOB_STATUS_CHOICE)
    resume = models.TextField(blank=True, null=True)
    is_manual_resume = models.BooleanField(default=False)
    cover_letter = models.TextField(blank=True, null=True)
    is_converted = models.BooleanField(default=False)
    converted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        default_permissions = ()
        db_table = "applied_job_status"
        ordering = ["id"]
        # unique_together = [("applied_by", "job")]

    def __str__(self):
        return self.applied_by.username


@receiver(post_save, sender=AppliedJobStatus)
def change_status(sender, instance, created, **kwargs):
    # set job_status to 1
    if created:
        # initial apply job_status will be 1
        instance.job_status = 1
        instance.save()


class BlacklistJobs(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        default_permissions = ()


class BlockJobCompany(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        default_permissions = ()


class SalesEngineJobsStats(TimeStamped):
    job_source = models.CharField(max_length=30, blank=True, null=True)
    jobs_count = models.IntegerField()


class JobUploadLogs(TimeStamped):
    jobs_count = models.IntegerField()


class TrendsAnalytics(TimeStamped):
    category = models.CharField(max_length=50, unique=True)
    tech_stacks = models.TextField(null=True, blank=True)

