from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .static import info
import json
from .forms import UrlForm

def home(req):
    return HttpResponse('Hello From Program')
    
def render_index(req):
  if req.method == 'GET':
    form = UrlForm()
    youtube_url = str(req.GET.get('url'))
    return render(req, 'program/index.html',{
        'version': info.program_config['version'],
        'received': youtube_url,
        'form':form
    })
  elif req.method == 'POST':
    form = UrlForm(req.POST)
    if form.is_valid():      
      text = form.cleaned_data['url']      
      form = UrlForm()
    print(text)
    args = {'version': info.program_config['version'],'form': form, 'text': text}      
    return render(req,'program/index.html', args)
    

def send_json(req):
    data = {"key":"value"}
    return JsonResponse(data)
    #return JsonResponse(json.dumps(data, ensure_ascii=False), safe=False)
    #return HttpResponse(json.dumps(data, ensure_ascii=False),content_type="application/json")
