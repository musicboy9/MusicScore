# -*- coding: cp949 -*-
import scipy.io.wavfile
import math


class WavFileModifier:# wav ������ �޾Ƶ��̴� class
    
    def __init__(self,wavFile):
        
        self.rate, self.wavArray = scipy.io.wavfile.read(wavFile)# �޾Ƶ��� wav ������ scipy�� read �Լ��� �̿��� rate�� numpy array ���·� object�� ����
        
