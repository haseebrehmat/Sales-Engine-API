import openai as openai
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import CompanyAPIIntegration

import settings.base


class GenerateCoverView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        name = request.data.get('name')
        job_des = request.data.get('job_des')
        company = request.data.get('company')
        experience = request.data.get('experience')
        conditions = [
            name is not None,
            job_des is not None,
            company is not None,
            experience is not None
        ]
        if all(conditions):
            obj = CompanyAPIIntegration.objects.filter(company=request.user.profile.company, name="chat gpt")
            if obj:
                openai.api_key = obj.first().api_key
            else:
                return Response({"detail": "Chat GPT integration is missing"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            try:
                keywords = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=(
                        f"Extract the keywords that can be used to write a cover letter from the following JOB description {job_des}"),
                    max_tokens=2000,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
            except:
                return Response({'detail': "Incorrect API key provided"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            keywords = keywords.choices[0].text
            completions = openai.Completion.create(
                engine="text-davinci-003",
                prompt=(f"Write a cover letter for {name} who want to apply at {company} having professioanl experience i-e {experience} containing the following keywords {keywords}"),
                max_tokens=3000,
                n=1,
                stop=None,
                temperature=0.7,
            )
            if len(completions.choices) > 0:
                message = completions.choices[0].text
                status_code = status.HTTP_200_OK
            else:
                message = "Something went wrong!"
        else:
            message = "Required fields cannot be empty"

        return Response({"detail": message}, status_code)
