import tqdm
from youtube_dl import YoutubeDL
import os
from tqdm import tqdm
import ffmpeg
BASE_DOWNLOAD_DIR = os.path.normpath(os.getcwd() + '/static/program/')
print("**** Download dir: ", BASE_DOWNLOAD_DIR)


bars = {}

def update_tqdm(information):
    filename = information['filename']
    try:
        downloaded = information['downloaded_bytes']
    except:
        if os.path.isfile(information['filename']+".m4a"):
          print("File already exists.")
        else:
          print("Error with:"+information['filename'])
    total = information['total_bytes'] or information['total_bytes_estimate']
    if downloaded and total:
        if filename not in bars:
            bars[filename] = tqdm(desc=filename[:10], unit='B', unit_scale=True, total=total)
        bar = bars[filename]
        bar.update(downloaded - bar.n)

def m4atowav(path):
    print("Converting{path.split['/'][-1]} to wav")
    stream = ffmpeg.input(path)
    out_name = path.split('.m4a')[0]+'.wav'
    out_stream = ffmpeg.output(stream, out_name ,f='wav')
    ffmpeg.run(out_stream)
    print(out_name)
    print("========Converted to wav========")
    return out_name.split('/static/')[1]

def download(url, prefix=''):
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

    file_noext = download_dir + prefix + title
    outfile = file_noext+'.m4a'
    file_wav = file_noext+'.wav'
    print("Start downloading ",url)
    print(outfile)
    if not os.path.isfile(outfile):
      ydl_setup.download([url])
      return m4atowav(outfile)
    elif not os.path.isfile(file_wav):
      print('***** File already downloaded, converting to wav: ', outfile)
      return m4atowav(outfile)
    else:
      print("**** Audio file(.wav) already exists: ",file_wav)
#download('https://www.youtube.com/watch?v=izGwDsrQ1eQ')
