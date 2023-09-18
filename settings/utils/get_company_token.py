from authentication.models import Team
from authentication.models.company import Company


def get_company_token(user_id):
    company = Company.objects.filter(user_id=user_id).first()
    if company is None:
        company = Company.objects.filter(user__teammanagement__reporting__exact=user_id).first()
    if company is not None:
        return company.name
    else:
        user = Team.objects.filter(user_id=user_id).first()
        if user is None:
            return False
        return get_company_token(user.id)


