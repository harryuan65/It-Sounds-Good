from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .static import info
import json

def home(req):
    return HttpResponse('Hello From Program')
    
def render_index(req):
    if req.method=='GET':
      youtube_url = str(req.GET.get('url'))
      return render(req, 'program/index.html',{# 1st way to insert template variables
        'version': info.program_config['version'],
        'query_received': youtube_url
      })
    elif req.POST: #the action done by submitting in form
      args ={}
      args['version'] = info.program_config['version']# 2nd way to insert template variables
      args['url_received'] = req.POST['url_input'] # Value got from form
      return render(req, "program/index.html", args)

def send_json(req):
    data = {"key":"value"}
    return JsonResponse(data)
    #return JsonResponse(json.dumps(data, ensure_ascii=False), safe=False)
    #return HttpResponse(json.dumps(data, ensure_ascii=False),content_type="application/json")
    #return HttpResponse(data,  'application/json')
