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
    response = serializers.SubmissionSerializer(data = body)
    if(response.is_valid()):
        inst = response.save()
        if(inst.inputGiven != ""):
            data = {'id' : inst.id, 'code' : inst.code, 'lang' : inst.language, 'inp' : inst.inputGiven, 'problemId' : inst.problemId}
        else:
            data = {'id' : inst.id, 'code' : inst.code, 'lang' : inst.language, 'problemId' : inst.problemId}
        q.append(inst.id)
        requests.post('https://judgeserver.herokuapp.com/run/', data = data)
        response = serializers.SubmissionSerializer(models.Submission.objects.get(id = inst.id))
        return Response(response.data)

    return Response(response.errors)
