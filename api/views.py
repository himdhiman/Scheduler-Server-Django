from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api import models
from api import serializers
import json
import requests
from collections import deque

# Create your views here.

q = deque()

@api_view(['POST'])
def run(request):
    body = json.loads(request.body)
    # print(request.body)
    # print(body)
    response = serializers.SubmissionSerializer(data = body)
    # print(response.data)
    if(response.is_valid()):
        inst = response.save()
        if(inst.inputGiven != ""):
            data = {'id' : inst.id, 'code' : inst.code, 'lang' : inst.language, 'inp' : inst.inputGiven}
        else:
            data = {'id' : inst.id, 'code' : inst.code, 'lang' : inst.language}
        q.append(inst.id)
        # print(inst.id)
        requests.post('http://judgeserver.herokuapp.com/run/', data = data)
        # print(out)
        response = serializers.SubmissionSerializer(models.Submission.objects.get(id = inst.id))
        # print(q)
        return Response(response.data)

    return Response(response.errors)
