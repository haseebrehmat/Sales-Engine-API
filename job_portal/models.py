import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from authentication.models import User
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
    tech_keywords = models.TextField(null=True, blank=True)
    job_posted_date = models.DateTimeField(null=True, blank=True)
    job_source_url = models.CharField(max_length=2000, null=True, blank=True)
    block = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=False)

    class Meta:
        default_permissions = ()
        db_table = "job_detail"
        unique_together = (('company_name', 'job_title'),)
        ordering = ['-job_posted_date']
        indexes = [models.Index(fields=['company_name', 'job_source', 'tech_keywords', 'job_posted_date'])]
        index_together = ['company_name', 'job_title']

    def __str__(self):
        return self.job_title


class AppliedJobStatus(models.Model):
    vertical = models.ForeignKey(Verticals, on_delete=models.SET_NULL, blank=True, null=True)

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
    # resume = models.TextField(blank=True, null=True)
    # cover_letter = models.TextField(blank=True, null=True)

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


# class UserAppliedJobs(TimeStamped):
