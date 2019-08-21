from .process import prediction

def execution(wav_path):
    print('\33[41m'+'Executing: '+wav_path +'\33[0m')
    return prediction.justdoit(wav_path)
    # return wav_path

