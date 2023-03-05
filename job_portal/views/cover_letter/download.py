# from authentication.models import TeamManagement
# from authentication.models.company import Company
#
# team = TeamManagement.objects.filter(user_id=request.user.id).first()
# print(team, team.reporting.name)
#
# if team.reporting.name is None:
#     company = Company.objects.filter(user_id=request.user.id).first()
#     print(company.name)
# else:
#     print(False)


from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from xhtml2pdf import pisa

from settings.utils.get_company_token import get_company_token


class DownloadCoverView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print(get_company_token(request.user.id))
        content = request.data.get("content", "")
        if content is not None:
            context = {
                "content": content.replace("\n", "<br>")
            }
            template = get_template("cover_letter.html")
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{request.data.get("name", "")} - cover.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            # if error then show some funny view
            if pisa_status.err:
                return HttpResponse(
                    {'detail': 'We had some errors <pre>' + html + '</pre>'},
                    content_type='application/json'
                )
            return response
        else:
            return HttpResponse(
                {'detail': 'Content cannot be empty'},
                content_type='application/json'
            )
