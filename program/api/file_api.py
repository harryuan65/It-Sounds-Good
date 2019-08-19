import os
from django.conf import settings
def printf(printstr):
  print('\33[94m'+printstr+'\33[0m')

def clearfiles(): 
  printf('================File Cleaner:Initializing===============')
  path = os.getcwd() + settings.STATIC_URL +'program/'
  printf('Checking unused files in :'+path)
  files = os.listdir(path)
  for f in files:
    if f.endswith('.m4a') or f.endswith('.wav') or f.endswith('.mp3'):
      printf('Deleted'+path + f)  
      os.remove(path + f)
  printf('================File Cleaner:Cleaned===================')


clearfiles()