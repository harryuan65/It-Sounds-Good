from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
import json
from .api import ydl_api
from .api import file_api
# from multiprocessing.pool import ThreadPool
# pool = ThreadPool(processes=2)
from .api import separate
import os
# from django.views import View
check = ''
args = {}
debugging = ''
# debugging='http://www.youtube.com/watch?v=2ZIpFytCSVc'
STATIC_DIR = os.path.normpath(os.getcwd() + '/static') +'/'
def static(filename):
  return STATIC_DIR+filename
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
        'url_received': False,
        'debugging': debugging
      })
    elif req.POST: #the action done by submitting in form
      if req.POST['url_input']:
        if check != req.POST['url_input']:
          print('\33[41m'+'POST: Got url'+'\33[0m')
          check = req.POST['url_input']
          file_wav, file_mp3 = ydl_api.download(req.POST['url_input'])
          args['url_received'] = req.POST['url_input'] # Value got from form
          args['downloaded_wav'] = file_wav
          args['downloaded_mp3'] = file_mp3
          args['wavfile'] = file_wav.split('.')[0]
          print('\33[5m'+'\33[0m')
          print('####### Downloaded file, -> html view:',file_wav)          
          print('####### Downloaded file, -> html view:',file_mp3)
          return render(req, "program/index.html", args)
        else:
          print(">>>>>Detected Refresh, please don't do it<<<<<<")
        return HttpResponseRedirect(reverse('index'))
      # else:
      #   print(">>>>>>Don't download empty url you punk<<<<<")
      #   return HttpResponseRedirect(reverse('index'))

def separation(req,wav_path):
  if req.method=="GET":
    #wav_path = req.GET.get('file_wav')
    #print("req.GET.get('file_wav') = " ,req.GET.get('file_wav'))
    filename = static(wav_path+'.wav')
    print('\33[43m'+'GET: Separation '+ filename+'\33[0m')
    # args['separated_wav'] =  debugging
    args['separated_wav'] = separate.execution(filename) or debugging
    return render(req,'program/separation.html',args)

def send_json(req):
    data = {"key":"value"}
    return JsonResponse(data)


# class LoadingView(View):
#   def get(self, request, *args):
#     return render(request,"program/loading.html",t)
  
