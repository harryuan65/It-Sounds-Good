import os
from django.conf import settings
def clearfiles(): 
  print('================File Cleaner:Initializing===============')
  path = os.getcwd() + settings.STATIC_URL +'program/'
  print('Checking unused files in :',path)
  files = os.listdir(path)
  for f in files:
    if f.endswith('.m4a') or f.endswith('.wav'):
      print('Deleted',path + f)  
      os.remove(path + f)
  print('================File Cleaner:Cleaned===================')


clearfiles()