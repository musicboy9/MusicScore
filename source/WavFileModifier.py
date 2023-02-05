# -*- coding: cp949 -*-
import scipy.io.wavfile
import math


class WavFileModifier:# wav 파일을 받아들이는 class
    
    def __init__(self,wavFile):
        
        self.rate, self.wavArray = scipy.io.wavfile.read(wavFile)# 받아들인 wav 파일을 scipy의 read 함수를 이용해 rate와 numpy array 형태로 object에 저장
        
