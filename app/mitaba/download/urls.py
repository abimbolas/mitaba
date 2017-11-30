from django.conf.urls import url
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.core.files.base import ContentFile

class ReportTextView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
      content = request.data['report']
      filename = request.query_params.get('filename')
      response = HttpResponse(ContentFile(content), content_type='application/octet-stream; charset=utf-8')
      response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
      return response

class ReportSpreadsheetView(APIView):
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = (JSONRenderer,)

    def get(self, request):
      temp_result = {
        'hello': 'world'
      }
      return Response(temp_result)

urlpatterns = [
  url(r'report-as-text', ReportTextView.as_view()),
  url(r'report-as-spreadsheet', ReportSpreadsheetView.as_view())
]
