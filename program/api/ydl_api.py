import tqdm
from youtube_dl import YoutubeDL
import os
from tqdm import tqdm
import ffmpeg

import threading
bars = {}
t = {'total':"-1",'downloaded':"0",'temp':"9"}
file_wav = ""
file_mp3 = ""
def printf(printstr):
  print('\33[4m'+printstr+'\33[0m')

def update_tqdm(information):
    filename = information['filename']
    try:
        downloaded = information['downloaded_bytes']
        total = information['total_bytes'] or information['total_bytes_estimate']
        t['total']=str(total)
        t['downloaded']=str(downloaded)
        if downloaded and total:
          if filename not in bars:
              bars[filename] = tqdm(desc=filename[:10], unit='B', unit_scale=True, total=total)
          bar = bars[filename]
          bar.update(downloaded - bar.n)
    except:
        if os.path.isfile(information['filename']+".m4a"):
          printf("File already exists.")
        else:
          printf("Error")
def remove_symbols(str_in):
  symbols = ['!','@','#','$','%','^',"&","*","`",' ','~']
  str_out = str_in
  for symbol in symbols:
    str_out = str_out.replace(symbol,'')
  return str_out
def convert(path,ext='wav'):
    print("\33[100m")
    try:
      stream = ffmpeg.input(path)
      out_name = path.split('.m4a')[0]+'.'+ext
      out_name = remove_symbols(out_name)
      print(" =============FFMPEG Converting ",path.split('/')[-1].split('.m4a')[0]," to ",ext,"=============")
      out_stream = ffmpeg.output(stream, out_name ,f=ext)
      ffmpeg.run(out_stream)
      printf(out_name)
      print('\33[6m')
      printf("=============Converted to {}=============".format(ext))
      result_name = out_name.split('/static/program/')[1]
      print('@@@@@@ ',result_name)
      print('\33[0m')
      return result_name
    except Exception as e:
      print("*****FFMpeg load Error:")
      print('====================',e,'======================')
      print('\33[0m')
    

def show_progress():
  while t['downloaded']!=t['total']:
    if t['temp']!=t['downloaded']:
      t['temp'] = t['downloaded'] 
      print("\33[92m"+"downloaded = "+t['downloaded']+", total = "+t['total']+"\33[0m")

  print("\33[42m"+"Finished"+"\33[0m")

def download(url, prefix=''):
  try:
    printf("=============Youtube Downloader: Initializing...========")
    file_wav = ""
    file_mp3 = ""
    BASE_DOWNLOAD_DIR = os.path.normpath(os.getcwd() + '/static/program') +'/'
    printf("**** Download dir: "+BASE_DOWNLOAD_DIR)
    printf("=============Youtube Downloader: Setting options")
    download_dir = BASE_DOWNLOAD_DIR

    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)

    ydl_opts = {
        'format': '140',
        'quiet': True,
        'progress_hooks': [
            update_tqdm,
        ],
        'outtmpl' : download_dir + prefix + '%(title)s.%(ext)s',
        'noplaylist': True
    }
    ydl_setup = YoutubeDL(ydl_opts)
    info_dict = ydl_setup.extract_info(url, download=False)
    title = info_dict.get('title', None)
    title = title.replace('/','_')
    file_noext = download_dir + prefix + title
    outfile = file_noext+'.m4a'
    file_wav = file_noext+'.wav'
    printf(">>>>>Start downloading "+url)
    if not os.path.isfile(outfile):
      x = threading.Thread(target=show_progress)
      x.start()
      ydl_setup.download([url])
      printf('****Downloaded '+outfile)
      file_wav = convert(outfile,'wav')
      file_mp3 = convert(outfile, 'mp3')
      
      x.join()
      return file_wav, file_mp3
    elif not os.path.isfile(file_wav):
      printf('***** File already downloaded, converting to wav: '+ outfile)
      file_wav = convert(outfile,'wav')
      file_mp3 = convert(outfile, 'mp3')
      return file_wav, file_mp3
    else:
      printf("**** Audio file(.wav) already exists: "+file_wav)
  except Exception as e:
    printf("****** Youtube Downloader went wrong")
    print('====================',e,'======================')
#download('https://www.youtube.com/watch?v=izGwDsrQ1eQ')
