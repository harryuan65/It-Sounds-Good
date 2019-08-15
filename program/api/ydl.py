import tqdm
import youtube_dl
import os
from tqdm import tqdm
import ffmpeg
import librosa
from IPython.display import Audio
BASE_DOWNLOAD_DIR = os.getcwd() + '/downloads/'

bars = {}

def update_tqdm(information):
    filename = information['filename']
    downloaded = information['downloaded_bytes']
    total = information['total_bytes'] or information['total_bytes_estimate']
    if downloaded and total:
        if filename not in bars:
            bars[filename] = tqdm(desc=filename[:10], unit='B', unit_scale=True, total=total)
        bar = bars[filename]
        bar.update(downloaded - bar.n)

def download(video_url, prefix=''):
    download_dir = BASE_DOWNLOAD_DIR + '/'

    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)

    ydl_opts = {
        'format': 'mp4',
        'quiet': True,
        'progress_hooks': [
            update_tqdm,
        ],
        'outtmpl' : download_dir + prefix + '%(title)s.%(ext)s'
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    ydl.download([video_url])
#download('https://www.youtube.com/watch?v=izGwDsrQ1eQ')
def mp4towav(path):
    stream = ffmpeg.input(path)
    out_stream = ffmpeg.output(stream, path.split('.')[0]+'.wav',f='wav')
    ffmpeg.run(out_stream)

path_test = BASE_DOWNLOAD_DIR+ 'George Michael - Careless Whisper (Official Video).mp4'
# mp4towav(path_test)

path_test_wav = BASE_DOWNLOAD_DIR+ 'George Michael - Careless Whisper (Official Video).wav'
#signal, sample_rate = librosa.load(path_test_wav)
# Audio(signal, rate=sample_rate)
