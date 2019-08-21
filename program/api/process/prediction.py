import librosa as librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import random
import pywt
from tqdm import tqdm
import scipy

import glob
import os

import tensorflow.keras as keras

dataArray = np.empty(shape=(0,65536),dtype = np.float64)
num_data = 0

def printf(printstr):
  print('\33[46m'+printstr+'\33[0m')

def printSizeInMb(dataIn, nameIn):
  import sys
  print("size of " + nameIn + "=" + str(sys.getsizeof(dataIn)/1000000) + "MB")


def printArrayInfo(arrayIn, arrayName):
  print("_")
  print(arrayName)
  print("shape " + str(arrayIn.shape))
  print("dtype " + str(arrayIn.dtype))
  print("max " + str(arrayIn.max()))
  print("min " + str(arrayIn.min()))
  print("_")
  
def plotAudio(audioIn, sampleRateIn):
  # import matplotlib.pyplot as plt
  # import librosa.display
  plt.figure(figsize=(15, 5))
  librosa.display.waveplot(audioIn, sampleRateIn, alpha=0.8)

#y_axis = "linear" or "log"
def plotSTFT(stft, sampleRate,hop_length, y_axis='linear'):

    librosa.display.specshow(librosa.amplitude_to_db(np.abs(stft)), y_axis=y_axis, x_axis='time', sr = sampleRate, hop_length=hop_length)
    plt.title('Power spectrogram')
    plt.colorbar(format='%+2.0f dB')
    plt.tight_layout()
    plt.show()
    
def plotMultipleSTFT(stftArray, stftArrayNoise, stftArray_reconstructed, sampleRate, hop_length, y_axis = 'linear'):
    #
    print("im inside")
    rows = stftArrayNoise.shape[0]
    plt.subplots(nrows=rows, ncols=3,figsize=(12,8))
    for i in range(stftArrayNoise.shape[0]):
      plt.subplot(rows, 3, i*3+1)
      librosa.display.specshow(librosa.amplitude_to_db(np.abs(stftArray[i])), y_axis=y_axis, x_axis='time', sr = sampleRate, hop_length=hop_length)
      plt.colorbar(format='%+2.0f dB')
      plt.title('orig. audio')
      plt.subplot(rows, 3, i*3+2)
      librosa.display.specshow(librosa.amplitude_to_db(np.abs(stftArrayNoise[i])), y_axis=y_axis, x_axis='time', sr = sampleRate, hop_length=hop_length)
      plt.colorbar(format='%+2.0f dB')
      plt.title('noise')
      plt.subplot(rows, 3, i*3+3)
      librosa.display.specshow(librosa.amplitude_to_db(np.abs(stftArray_reconstructed[i])), y_axis=y_axis, x_axis='time', sr = sampleRate, hop_length=hop_length)
      plt.colorbar(format='%+2.0f dB')
      plt.title('reconstructed')
    plt.tight_layout()
    plt.show()


    
def plot_history_graphs(history, string):
    # summarize history for loss
    # import matplotlib.pyplot as plt
    plt.plot(history.history[string])
    plt.plot(history.history['val_'+string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.legend(['train ' + string, 'test ' + 'val_'+string])
    plt.show()

class Config:
  def __init__(self, n_fft = 4096, win_length = 4096, hop_length = 1024, sampleRate = 44100):
  #def __init__(self, n_fft = 2048, win_length = 2048, hop_length = 512, sampleRate = 8000):
  #def __init__(self, n_fft = 1536, win_length = 1536, hop_length = 384, sampleRate = 8000):
  #def __init__(self, n_fft = 1024, win_length = 1024, hop_length = 256, sampleRate = 8000):
#>> 1024 - got good result both for 8000 and 16000 sr, conv = 3,3
  #def __init__(self, n_fft = 256, win_length = 256, hop_length = 64, sampleRate = 8000):
    self.n_fft = n_fft
    self.win_length = win_length
    self.hop_length = hop_length
    self.sampleRate = sampleRate
    
config = Config()

waveName = 'dmey'

#convert to stft
def __trimApprox(coeffs_full):
      from tqdm import tqdm
      #print("trim data")
      coeffs_trimmed = []
      coeffs_trimmed.append(coeffs_full[0][0])
      for coeff in tqdm(coeffs_full):
          coeffs_trimmed.append(coeff[1])
      return coeffs_trimmed

def wavelet(dataArrayIn,waveName):
  # import pywt
  # import numpy as np

  coeffsLists = []
  for data in dataArrayIn:
    temp = pywt.swt(data,waveName,level = 1)
#     printArrayInfo(np.array(temp),"temp")
    trim = __trimApprox(temp)
    coeffsLists.append(trim)
       
  printArrayInfo(np.array(coeffsLists),"coeffsLists")
  
  #normalize
  coeffsArray = np.transpose(np.array(coeffsLists),(0,1,2))
#   printArrayInfo(coeffsArray,"coeffsArray with transpose")
  return coeffsArray

def MagPhase(stftArrayIn):
  # import numpy as np
  # import librosa as librosa
  #get magnitudes and phases from STFT
  
  magnitudesList = []
  phasesList = []
  for stft in stftArrayIn:
    mag,phase = librosa.magphase(stft)
    magnitudesList.append(mag)
    phasesList.append(phase)
  
  magnitudesArray = np.array(magnitudesList)
  phasesArray = np.array(phasesList)

  #normalize (each layer has different normalization)
  tempArray = np.transpose(magnitudesArray,(1,0,2,3))
  Normalization = []
  for data in tempArray:
    normax = data.max()
    m = int(normax)+1
    Normalization.append(m)

  # print("normalization ",Normalization)

  return magnitudesArray, phasesArray,Normalization

def layer_STFT(coeffsArrayIn):
  # import librosa
  # import numpy as np
  stft = librosa.stft(coeffsArrayIn[0][0],n_fft = 4096, win_length = 4096, hop_length = 1024)
  stftArray = np.empty(shape = (coeffsArrayIn.shape[0],coeffsArrayIn.shape[1],stft.shape[0],stft.shape[1]), dtype = stft.dtype)
  
  i=0
  for data in coeffsArrayIn:
    j=0
    for layer in data:
      temp =librosa.stft(layer,n_fft = 4096, win_length = 4096, hop_length = 1024)
      #printArrayInfo(layer,"layer")
      #printArrayInfo(temp,"temp")
      stftArray[i][j]=temp
      j+=1
    i+=1
  #printArrayInfo(stftArray,"stftArray")
  magnitudesArray, phasesArray,normalization = MagPhase(stftArray)
  #printArrayInfo(stftArray,"stftArray")
  return stftArray,magnitudesArray,phasesArray,normalization
      
#reconstruct
def STFTarrayToCoeffs(stftArrayIn, sampleRateIn):
  global dataArray
  # import librosa
  # import numpy as np
  # from tqdm import tqdm
  #import scipy

  signal_rec = librosa.istft(stftArrayIn[0][0],
                             #n_fft=config.n_fft,
                             hop_length=config.hop_length,
                             win_length=config.win_length,
                             center = False,
                             window=scipy.signal.hamming,
                             length = dataArray.shape[1]
                            )
  print("sig.  ",signal_rec.shape,"\n\n\n")
  coeffsArray_rec = np.empty(shape = (stftArrayIn.shape[0],stftArrayIn.shape[1], signal_rec.shape[0]), dtype=signal_rec.dtype)
 
  
  i=0
  for stft in stftArrayIn:
    
    j=0
    for data in stft:
      coeffsArray_rec[i][j] = librosa.istft(data,
                                     #n_fft = config.n_fft,
                                     hop_length=config.hop_length,
                                     win_length=config.win_length,
                                     center = False,
                                     window=scipy.signal.hamming,
                                     length = dataArray.shape[1]
                                           )
      j+=1
    i+=1  
    
  # printArrayInfo(coeffsArray_rec,"istft == reconstructed coeffsArray(trimmed)")
  return coeffsArray_rec

def inv_magphase(mag, phase):
  #import numpy as np
  #phase = np.cos(phase_angle) + 1.j * np.sin(phase_angle)
  return mag * phase

def processPredictedData(magArrayIn, phasesArrayIn,normalArrayIn):
  import numpy as np
  
  #normalize
  for i in range(magArrayIn.shape[0]):
    magArrayIn[i] = magArrayIn[i] * normalArrayIn[i]

  print('reshape from conv')
  magArrayIn = np.transpose(magArrayIn,(1,0,2,3,4))
  magArrayIn = np.reshape(magArrayIn,(magArrayIn.shape[0],magArrayIn.shape[1],magArrayIn.shape[2],magArrayIn.shape[3]))
  # printArrayInfo(magArrayIn,"magArrayIn")

  #arraySTFTOut = getSTFTfromMagAndPhase(magArrayIn, phasesArrayIn)
  arraySTFTOut = inv_magphase(magArrayIn, phasesArrayIn)
  dataArrayOut = STFTarrayToCoeffs(arraySTFTOut, config.sampleRate)
  
  
  
  
  return magArrayIn, arraySTFTOut, dataArrayOut

def __iswtFromTrimmed(coeffs_trimmed,waveName):
    # import pywt
    # import numpy as np
    
    coeff_full = []
    A_prev = coeffs_trimmed[0]
    for layer in range(len(coeffs_trimmed) - 1):
        layer_coeff = []
        layer_coeff.append([A_prev, coeffs_trimmed[layer + 1]])
        A = pywt.iswt(coeffs=np.array(layer_coeff), wavelet=waveName)
        coeff_full.append([A, coeffs_trimmed[layer + 1]])
        A_prev = A
    audio_rec = pywt.iswt(coeff_full, wavelet=waveName) 
#     printArrayInfo(np.array(coeff_full),"ddd")  
#     printArrayInfo(np.array(audio_rec),"rec")

    return audio_rec

#iswt  
def iWavelet(ArrayIn,waveName):
  # import numpy as np
  # import pywt
  # from tqdm import tqdm
  
#   #reshape
#   ArrayIn = np.transpose(ArrayIn,(0,3,1,2))
#   print(ArrayIn.shape)
  
  recArray = np.empty(shape=(ArrayIn.shape[0],ArrayIn.shape[2]))
  i=0
  for data in tqdm(ArrayIn):
    recArray[i] = __iswtFromTrimmed(data,waveName)
    i+=1
  # printArrayInfo(recArray,"reconstructed Array")
  
  return recArray



#========================================================================================

#load
def justdoittest(path):
  original_name = path.split('/')[-1]
  outname = original_name.split('.')[0]+'_proc_'+'.wav'
  outpath = path.split(original_name)[0] + outname
  printf("original name = "+original_name)
  printf('Outname = '+outname)
  printf('Model processed: '+outpath)
  return outname
def justdoit(path):
  global data, dataArray, num_data
  BASE_DIR = os.path.normpath(os.getcwd() + '/program/api/process') +'/'
  printf('Model processing file:'+path)
  data,sample_rate = librosa.load(path,sr=44100)
  
  num_data = int(data.shape[0]/65536)
  print(data.shape)
  print(num_data)
  
  data_trim = data[:num_data*65536]
  librosa.output.write_wav("./data_trim.wav",data_trim,sr=sample_rate)
  
  dataArray = np.empty(shape=(num_data,65536),dtype = data.dtype)
  
  for i in range(num_data):
    dataArray[i] = data[i*65536:(i+1)*65536]
  # print(dataArray.shape)
  # print(dataArray.dtype)
  
  coeffsArray = wavelet(dataArray,waveName)
  
  stftArray,magnitudesArray,phasesArray,normalization = layer_STFT(coeffsArray)
  
  # print("info")
  # printArrayInfo(coeffsArray,"coeffsArray")
  # printArrayInfo(stftArray,"stftArray")
  # printArrayInfo(magnitudesArray,"magnitudesArray")
  # printArrayInfo(phasesArray,"phasesArray")
  # print(normalization)
  
  #normalize to cnn
  magnitudesArray = np.transpose(magnitudesArray,(1,0,2,3))
  
  #normalize
  for i in range(magnitudesArray.shape[0]):
    magnitudesArray[i] = magnitudesArray[i]/float(normalization[i])
    
  magnitudesArray = np.reshape(magnitudesArray,(magnitudesArray.shape[0],magnitudesArray.shape[1],magnitudesArray.shape[2],magnitudesArray.shape[3],1))
  
  printArrayInfo(magnitudesArray,"magnitudesArray before cnn")
  
  #predict
  model1 = keras.models.load_model(BASE_DIR+'layer1_500.h5')
  # model1.summary()
  model2 = keras.models.load_model(BASE_DIR+'layer2_500.h5')
  # model2.summary()
  
  layer1_pre = model1.predict(magnitudesArray[0],verbose = 1)
  layer2_pre = model2.predict(magnitudesArray[1],verbose = 1)
  
  predictedArray = np.empty(shape = (magnitudesArray.shape[0],
                                     magnitudesArray.shape[1],
                                     magnitudesArray.shape[2],
                                     magnitudesArray.shape[3],
                                     magnitudesArray.shape[4]),
                            dtype = magnitudesArray.dtype)
  predictedArray[0]=layer1_pre
  predictedArray[1]=layer2_pre
  
  # printArrayInfo(predictedArray,"predictedArray")
  
  magnitudesArray_reconstructed, stftArray_reconstructed, coeffsArray_reconstructed = processPredictedData(predictedArray,phasesArray,normalization)
  
  # printArrayInfo(magnitudesArray_reconstructed,"magnitudesArray_reconstructed")
  # printArrayInfo(stftArray_reconstructed,"stftArray_reconstructed")
  # printArrayInfo(coeffsArray_reconstructed,"coeffs")
  
  recArray= iWavelet(coeffsArray_reconstructed,waveName)
  # printArrayInfo(recArray,"recArray")
  
  #conbine all array into an audio
  total = recArray.shape[0] * 65536
  audio = np.empty(shape = (total),dtype = data.dtype)
  
  for i in range(recArray.shape[0]):
    audio[i*65536:(i+1)*65536] = recArray[i]
    
  # printArrayInfo(data,"data")
  # printArrayInfo(audio,"audio")
  
  # print("sr : ",sample_rate)
  original_name = path.split('/')[-1]
  outname = original_name.split('.')[0]+'_proc_'+'.wav'
  outpath = path.split(original_name)[0] + outname
  printf("original name = "+original_name)
  printf('Outname = '+outname)
  printf('Model processed: '+outpath)
  librosa.output.write_wav(outpath,audio,sr=sample_rate)
  return outname

