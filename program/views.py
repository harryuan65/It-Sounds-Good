from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
import json
from .api import ydl_api
from .api import file_api
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=2)
import threading
# from django.views import View
check = ''
args = {}
x = threading.Thread()

def home(req):
    return HttpResponse('Hello From Program')
    
def index(req):
    global check, args
    if req.method=='GET':
      file_api.clearfiles()
      check = ''
      youtube_url = str(req.GET.get('url'))
      return render(req, 'program/index.html',{# 1st way to insert template variables
        'query_received': youtube_url,
        'url_received': False
      })
    elif req.POST: #the action done by submitting in form
      if req.POST['url_input']:
        if check != req.POST['url_input']:
          print('\33[41m'+'POST: Got url'+'\33[0m')
          check = req.POST['url_input']
          async_result = pool.apply_async(ydl_api.download, (req.POST['url_input'], ''))
          file_wav, file_mp3 = async_result.get()
          args['url_received'] = req.POST['url_input'] # Value got from form
          args['downloaded_wav'] = file_wav
          args['downloaded_mp3'] = file_mp3
          print('####### Downloaded file, -> html view:',file_wav)          
          print('####### Downloaded file, -> html view:',file_mp3) 
          async_result2 = pool.apply_async(render,(req, "program/index.html", args))
          return async_result2.get()
        else:
          print(">>>>>Detected Refresh, please don't do it<<<<<<")
        return HttpResponseRedirect(reverse('index'))
      else:
        print(">>>>>>Don't download empty url you punk<<<<<")
        return HttpResponseRedirect(reverse('index'))


def send_json(req):
    data = {"key":"value"}
    return JsonResponse(data)


# class LoadingView(View):
#   def get(self, request, *args):
#     return render(request,"program/loading.html",t)
  
