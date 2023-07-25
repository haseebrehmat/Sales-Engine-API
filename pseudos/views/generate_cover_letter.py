from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from job_portal.models import JobDetail
from pseudos.models import CoverLetter, Verticals
from utils.regex.backend import backend_regex
from utils.regex.devops import devops_regex
from utils.regex.frontend import frontend_regex
from utils.regex.core_framework import core_framework_regex
from utils.regex.get_skills import get_skills
from utils.regex.core_framework import tech
from utils.regex.database import database
from utils.regex.libraries import libraries
from utils.regex.tools import tools


class GenerateCoverLetter(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        vertical_id = request.GET.get("vertical_id")
        job_id = request.GET.get("job_id")
        status_code = status.HTTP_406_NOT_ACCEPTABLE

        if vertical_id is None:
            data = {"detail": "Vertical ID cannot be empty"}
        if job_id is None:
            data = {"detail": "Job ID cannot be empty"}
        else:
            job_data = JobDetail.objects.filter(id=job_id).first()
            cover_letter = CoverLetter.objects.filter(vertical_id=vertical_id).first()
            vertical = Verticals.objects.filter(id=vertical_id).first()

            if job_data is None:
                data = {"detail": "Invalid Job ID or Vertical ID"}

            elif cover_letter is None:
                data = {"detail": "Cover letter not available"}

            else:
                template = cover_letter.template
                cover_letter = self.cover_letter_context(template, job_data, vertical)
                if cover_letter:
                    data = {
                        "cover_letter": cover_letter,
                        "vertical_id": vertical_id
                    }
                    status_code = status.HTTP_200_OK
                else:
                    data = {"detail": "Failed to create cover letter"}
                    status_code = status.HTTP_406_NOT_ACCEPTABLE

        return Response(data, status=status_code)

    def cover_letter_context(self, template, job, vertical):
        print(f"Job description is : {job.job_description} \n")
        print("template => ", template)
        empty = []
        back_side_skills = get_skills(job.job_description, backend_regex, empty)
        # if not back_side_skills:
        #     return False
        print(f"Back side skills are: {back_side_skills}\n")
        front_side_skills = get_skills(job.job_description, frontend_regex, empty)
        # if not front_side_skills:
        #     return False
        print(f"Front side skills are : {front_side_skills} \n")
        devops_side_skills = get_skills(job.job_description, devops_regex, empty)
        # if not devops_side_skills:
        #     return False
        print(f"Devops skills are : {devops_side_skills} \n")
        core_side_skills = get_skills(job.job_description, core_framework_regex, tech)
        # if not core_side_skills:
        #     return False
        print(f"Core skills are : {core_side_skills} \n")
        database_side_skills = get_skills(job.job_description, empty, database)
        # if not database_side_skills:
        #     return False
        print(f"Data base skills are : {database_side_skills}\n")
        library_side_skills = get_skills(job.job_description, empty, libraries)
        # if not library_side_skills:
        #     return False
        print(f"Library skills are : {library_side_skills}\n")
        tools_side_skills = get_skills(job.job_description, empty, tools)
        # if not tools_side_skills:
        #     return False
        print(f"Tools side skills are : {tools_side_skills}\n")

        back_side_skills = list(dict.fromkeys(back_side_skills))
        front_side_skills = list(dict.fromkeys(front_side_skills))
        devops_side_skills = list(dict.fromkeys(devops_side_skills))
        core_side_skills = list(dict.fromkeys(core_side_skills))
        database_side_skills = list(dict.fromkeys(database_side_skills))
        library_side_skills = list(dict.fromkeys(library_side_skills))
        tools_side_skills = list(dict.fromkeys(tools_side_skills))

        frontend_skills = f"{', '.join(front_side_skills)}\n"
        devops_skills = f"{', '.join(devops_side_skills)}\n"
        backend_skills = f"{', '.join(back_side_skills)}\n"
        core_side_skills = f"{', '.join(core_side_skills)}\n"
        database_side_skills = f"{', '.join(database_side_skills)}\n"
        library_side_skills = f"{', '.join(library_side_skills)}\n"
        tools_side_skills = f"{', '.join(tools_side_skills)}\n"


        dynamic_keys = {
            '@name@': vertical.name,
            '@job_title@': job.job_title,
            '@company_name@': job.company_name,
            '@client_side_skills@': frontend_skills,
            '@server_side_skills@': backend_skills,
            '@core_side_skills@': core_side_skills,
            '@devops_side_skills@': devops_skills,
            '@database_side_skills@': database_side_skills,
            '@libraries_side_skills@': library_side_skills,
            '@tools_side_skills@': tools_side_skills,
            '@years_of_experience@': "5 Years"
        }

        for x in dynamic_keys.keys():
            if x in template:
                template = template.replace(x, dynamic_keys[x])
        return template
