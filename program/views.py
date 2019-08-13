from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

def home(req):
    return HttpResponse('Hello From Program')
    
def render_index(req):
    return render(req, 'program/index.html',{
        'title': 'Newest Version'
    })

def send_json(req):
    data = {"key":"value"}
    return JsonResponse(data)
    #return JsonResponse(json.dumps(data, ensure_ascii=False), safe=False)
    #return HttpResponse(json.dumps(data, ensure_ascii=False),content_type="application/json")
    #return HttpResponse(data,  'application/json')
# Create your views here.
