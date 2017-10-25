from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseBadRequest
import requests

petrov = 'http://82.196.2.175:8062/timer/'

class PetrovView(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        if 'account' in request.query_params:
            account = request.query_params['account']
            result = requests.get(petrov + account  + '/')
            return Response(result.json())
        else:
            return HttpResponseBadRequest('<h1>Bad Request</h1><p>Provide \"?account=my-sample-account\" query param</p>')
