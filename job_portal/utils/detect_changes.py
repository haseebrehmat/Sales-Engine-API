from candidate.models import Candidate
from job_portal.models import EditHistory
from lead_management.models import Phase, CompanyStatus


def detect_model_changes(instance, updated_instance, model, user):
    model_name = model.__name__
    change_logs = []
    if model_name == 'JobDetail':
        for x in updated_instance.keys():
            old_value = str(getattr(instance, x))
            new_value = str(updated_instance[x])
            if old_value != new_value:
                change_logs.append({"field": x, "old_value": old_value, "new_value": new_value})
        if len(change_logs) > 0:
            try:
                EditHistory.objects.create(instance_id=instance.id, model=model_name, changes=change_logs,
                                           user=user,
                                           company_id=user.profile.company_id)
            except:
                print("")
    elif model_name == 'Lead':
        for x in updated_instance.keys():
            old_value = str(instance[x])
            new_value = str(updated_instance[x])
            if old_value != new_value:
                if x == 'candidate_id':
                    change_logs.append({"field": "candidate", "old_value": 'None' if old_value == 'None' else
                    Candidate.objects.filter(id=old_value).first().name,
                                        "new_value": Candidate.objects.filter(id=new_value).first().name})
                elif x == 'phase_id':
                    change_logs.append({"field": "phase", "old_value": 'None' if old_value == 'None' else
                    Phase.objects.filter(id=old_value).first().name,
                                        "new_value": Phase.objects.filter(id=new_value).first().name})
                elif x == 'company_status_id':
                    company_status_new = CompanyStatus.objects.filter(id=new_value).first()
                    company_status_old = CompanyStatus.objects.filter(id=old_value).first()
                    change_logs.append({"field": "company_status", "old_value": company_status_old.status.name,
                                        "new_value": company_status_new.status.name})
                else:
                    change_logs.append({"field": x, "old_value": old_value, "new_value": new_value})
        if len(change_logs) > 0:
            try:
                EditHistory.objects.create(instance_id=instance['id'].id, model=model_name, changes=change_logs,
                                           user=user,
                                           company_id=user.profile.company_id)
            except:
                print("")
