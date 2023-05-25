from django.db import models

from authentication.models import User
from authentication.models.company import Company
from candidate.models.candidate import Candidate
from utils.model_fields.timestamped import TimeStamped


class CandidateLogs(TimeStamped):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL)
    exposed_user = models.ForeignKey(Candidate, on_delete=models.SET_NULL)
    exposed_to = models.ForeignKey(Company, on_delete=models.SET_NULL)

