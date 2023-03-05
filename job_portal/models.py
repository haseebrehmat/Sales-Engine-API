import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from authentication.models import User
from authentication.models.company import Company
from job_portal.utils.job_status import JOB_STATUS_CHOICE
from settings.utils.model_fields import TimeStamped


class JobDetail(models.Model):
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
    job_status = models.IntegerField(default=0, choices=JOB_STATUS_CHOICE)

    class Meta:
        default_permissions = ()
        db_table = "job_detail"
        unique_together = (('company_name', 'job_title'),)
        ordering = ['-job_posted_date']
        indexes = [models.Index(fields=['company_name','job_source','tech_keywords','job_posted_date'])]
        index_together = ['company_name', 'job_title']

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
        default_permissions = ()
        db_table = "applied_job_status"
        ordering = ["id"]

    def __str__(self):
        return self.applied_by.username


@receiver(post_save, sender=AppliedJobStatus)
def change_status(sender, instance, created, **kwargs):
    #set job_status to 1
    if created:
        JobDetail.objects.filter(id=instance.job_id).update(job_status=1)


class BlacklistJobs(TimeStamped):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    compnay_name = models.CharField(max_length=100,blank=True,null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    class Meta:
        default_permissions = ()