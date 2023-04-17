from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from pseudos.models import Verticals, Skills, Experience, Education, Links, Language, OtherSection, Projects


class ResumeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        vertical = Verticals.objects.filter(pk=pk).first()
        data = dict()
        data['basic_info'] = {
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
        skills = Skills.objects.filter(vertical_id=pk)
        data["skills"] = [{"name": skill.name, "level": skill.level} for skill in skills]

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
