from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
import json
from .api import ydl_api
from .api import file_api
# from .forms import UploadFileForm
# from .api import file_api
check = ''
def home(req):
    return HttpResponse('Hello From Program')
    
def render_index(req):
    global check
    file_api.clearfiles()
    if req.method=='GET':
      check = ''
      youtube_url = str(req.GET.get('url'))
      return render(req, 'program/index2.html',{# 1st way to insert template variables
        'query_received': youtube_url,
        'url_received': False
      })
    elif req.POST: #the action done by submitting in form
      args = {}
      if req.POST['url_input']:
        if check != req.POST['url_input']:
          check = req.POST['url_input']
          filename = ydl_api.download(req.POST['url_input'])
          args['url_received'] = req.POST['url_input'] # Value got from form
          args['downloaded_wav'] = filename
          print('####### Downloaded file, -> html view:',filename)          
          return render(req, "program/index2.html", args)
        else:
          print(">>>>>Detected Refresh, please don't do it<<<<<<")
          return HttpResponseRedirect(reverse('render_index'))
      else:
        print(">>>>>>Don't download empty url you punk<<<<<")
        return HttpResponseRedirect(reverse('render_index'))

def send_json(req):
    data = {"key":"value"}
    return JsonResponse(data)
    #return JsonResponse(json.dumps(data, ensure_ascii=False), safe=False)
    #return HttpResponse(json.dumps(data, ensure_ascii=False),content_type="application/json")
    #return HttpResponse(data,  'application/json')

# def upload_file(request):
#     if request.method == 'POST':
#       form = UploadFileForm(request.POST or None, request.FILES or None)
#       print('POST THIs FORM')
#       if form.is_valid():
#         file_api.handle_uploaded_file(request.FILES['file'])
#         form.save()
#         args={}
#         args['notice']="Uploaded Success"
#         return render(request,'program/upload_file.html', args)
#       else:
#         return HttpResponse(form.errors)
#     else:
#       form = UploadFileForm()
#       return render(request, 'program/upload_file.html',{'form':form})