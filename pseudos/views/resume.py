from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pseudos.models import Verticals, Skills, Experience, Education, Links, Language, OtherSection, Projects


class ResumeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        vertical = Verticals.objects.filter(pk=pk).first()
        if vertical is None:
            return Response({"detail": "Resume details not found"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = dict()
        data['basic'] = {
            "name": vertical.name,
            "hidden": vertical.hidden,
            "email": vertical.email,
            "phone": vertical.phone,
            "address": vertical.address,
            "designation": vertical.designation,
            "avatar": vertical.avatar,
            "portfolio": vertical.portfolio,
            "description": vertical.description
        }

        data["summary"] = vertical.summary
        data["hobbies"] = "" if len(vertical.hobbies) == 0 else vertical.hobbies.split(",")
        skills_all = Skills.objects.filter(vertical_id=pk)
        skills_client_side = skills_all.filter(generic_skill__type='clientside')
        skills_server_side = skills_all.filter(generic_skill__type='serverside')
        skills_devops = skills_all.filter(generic_skill__type='devops')
        skills_others = skills_all.filter(generic_skill__type='others')
        data["skills"] ={"all" : [{"name": skill.generic_skill.name, "level": skill.level} for skill in skills_all],
                         "clientside" : [{"name": skill.generic_skill.name, "level": skill.level} for skill in skills_client_side],
                         "serverside": [{"name": skill.generic_skill.name, "level": skill.level} for skill in skills_server_side],
                         "devops": [{"name": skill.generic_skill.name, "level": skill.level} for skill in skills_devops],
                         "others": [{"name": skill.generic_skill.name, "level": skill.level} for skill in skills_others],
                         }

        experience = Experience.objects.filter(vertical_id=pk)
        data["experience"] = [{
            "company": x.company_name,
            "title": x.designation,
            "from": x.start_date,
            "to": x.end_date,
            "description": x.description,
        } for x in experience]

        education = Education.objects.filter(vertical_id=pk)
        data["education"] = [{
            "institute": x.institute,
            "degree": x.degree,
            "from": x.start_date,
            "to": x.end_date,
            "grade": x.grade
        } for x in education]

        links = Links.objects.filter(vertical_id=pk)
        temp = {}
        for x in links:
            temp[x.platform] = x.url
        data["links"] = temp

        languages = Language.objects.filter(vertical_id=pk)
        data["languages"] = [{"name": x.name, "level": x.level} for x in languages]

        others = OtherSection.objects.filter(vertical_id=pk)
        data["others"] = [{"name": x.name, "value": x.value} for x in others]
        projects = Projects.objects.filter(vertical_id=pk)
        projects = [{"name": x.name, "title": x.title, "description": x.description, "repo": x.repo}
                    for x in projects]
        data["projects"] = projects
        return Response(data)
