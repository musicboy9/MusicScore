# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:03:16 2016

@author: INTER
"""
import matplotlib.pyplot as plt
import numpy as np
from WavFileModifier import *

 ## need to import matplotlib.pyplot as plt
 ## need to import numpy as np
def FFTmanual(input_list, audiorate, precision): #numpy list, audiorate, precision을 input으로 받아 fft 함수를 통해 frequency list(xx)와 intensity list(yy)를 return한다.
    k = np.fft.fft(input_list, precision)#numpy fft function - complex number list를 return함(k)
    xx = [None]*(len(k)/2)#2로 나누어주는 이유는 complex number라서 길이가 2배로 인식됨
    yy = [None]*(len(k)/2)
    for i in range(len(k)/2):
        yy[i] = np.abs(k[i])#intensity list에 append
        xx[i] = i/float(len(k))*audiorate#frequency list에 append
    return xx, yy

def noteGenerator(wavFileNameInput): # 프로그램과 같은 위치에 있는 wav 파일의 이름을 input으로 받아 어느 frequency의 음이 상대적 길이로 얼마동안 유지되는지 [음,길이]의 list의 list로 return함
    wavFileModifier = WavFileModifier(wavFileNameInput+".wav") # wav 파일을 받아들이는 WavFileModifier Object 생성
    modifiedList=[None]*5000
    freqList = []

    #fft 함수를 array의 원소 5000개에 대해서 진행하고, 1000개씩 index를 추가하면서 함수를 반복한다.
    
    for i in range(int(len(wavFileModifier.wavArray)/1000)-5):
        for j in range(5000):
            modifiedList[j]=(wavFileModifier.wavArray[j+i*1000][1])#5000개의 원소를 modifiedList에 저장
        xx, yy = FFTmanual(modifiedList,wavFileModifier.rate,10000)#modifiedList에 대해 fft함수를 진행
        c=0#index
        maxi=0#max intensity
        maxf=0#max frequency
        #주어진 frequency의 list에 대해 가장 intensity가 큰 frequency를 그 순간의 음이라고 판단함. 추후에 화음을 추가하기 위해서는 이 부분을 수정해야함.
        while(xx[c]<5000):#5000Hz보다 큰 음에 대해서는 무시함
            if yy[c]>maxi :#가장 큰 intensity를 발견했을 때
                maxi=yy[c]
                maxf=xx[c]#frequency를 업데이트
            c+=1
        freqList.append(maxf)# frequency들의 list에 append

    #음표의 위치를 지정해주기 위해 intensity의 list를 생성, avgnum1개씩 원소를 잡아서 index를 1개씩 밀면서  평균을 낸다. 또한, 평균을 낸 list를 다시 avgnum2개씩 원소를 잡아 같은 과정을 반복한다.
    #이때, 같은 index에 대해 두번째 list가 첫번째 list보다 크다가 대소관계가 바뀌는 곳을 음표의 위치라고 판단했다.
    
    intensityList = [None]*len(wavFileModifier.wavArray)#intensity list를 생성
    for j in range(len(wavFileModifier.wavArray)):
        intensityList[j]=wavFileModifier.wavArray[j][1]**2#각각의 index에 대해 intensity를 append
    
    finalIntensityList = [0]*len(wavFileModifier.wavArray)
    finalIntensityList[0]=0
    avgNum1 = 3900
    for j in range(0, avgNum1):
        finalIntensityList[0]+=intensityList[j]/float(avgNum1)#avgNum1개수만큼 평균을 잡아서 append
    for j in range(1, len(wavFileModifier.wavArray)-avgNum1):
        finalIntensityList[j] = finalIntensityList[j-1] - intensityList[j-1]/float(avgNum1) + intensityList[j+avgNum1-1]/float(avgNum1)#전 원소에서 앞의 원소만큼의 부분을 빼고 다음 원소만큼을 더해줌
        
    #finalIntensityList에 대해서 같은 과정을 반복해 secondIntensityList 생성
    secondIntensityList = [None]*len(wavFileModifier.wavArray)
    secondIntensityList[0]=0
    avgNum2 = 2900
    for j in range(0, avgNum2):
        secondIntensityList[0]+=finalIntensityList[j]/float(avgNum2)
    for j in range(1, len(finalIntensityList)-avgNum2):
        secondIntensityList[j] = secondIntensityList[j-1] - finalIntensityList[j-1]/float(avgNum2) + finalIntensityList[j+avgNum2-1]/float(avgNum2)

    compareList = [None]*len(wavFileModifier.wavArray)#같은 index에 대해 비교하는 list 생성
    for i in range(len(compareList)):
        if (finalIntensityList[i]>secondIntensityList[i]) and (finalIntensityList[i]>400000):#finalIntensityList의 원소가 secondIntensityList보다 크고 finalIntensityList의 원소가 400000보다 클때
            compareList[i] = 800000#compareList의 원소를 800000으로 바꾸어줌
        else:
            compareList[i] = 0
    
    peakList = []
    #compareList가 800000으로 바뀌고 100개 index에 대해 유지되면 peak이고, 그 peak의 index를 peakList에 추가해줌
    
    for index in range(len(compareList)-100):
        if index == 0:
            temp = True
            for k in range(100):
                if compareList[index+k] != 800000:
                    temp = False
            if temp:
                peakList.append(index)
        if compareList[index] == 0:
            temp = True
            for k in range(1,100):
                if compareList[index+k] != 800000:
                    temp = False
            if temp:
                peakList.append(index)
    
    finalFreqList = []
    #각 peak에 해당하는 frequency를 저장하는 list
    '''
    for peak in peakList:
        index = int(peak/1000)+3
        if index >= len(freqList)-1:
            finalFreqList.append(freqList[-1])
        else:
            finalFreqList.append(freqList[index+1])
    '''            
    for peakIndex in range(len(peakList)):
        if peakIndex == len(peakList)-1:
            finalFreqList.append(freqList[-1])#마지막 peak는 마지막 freq를 추가
        else:
            index1 = int(peakList[peakIndex]/1000)
            index2 = int(peakList[peakIndex+1]/1000)
            if index2 >= len(freqList)-1:
                finalFreqList.append(freqList[-1])#index가 frequency list의 index를 벗어날 경우 마지막 freq를 추가(frequency list는 평균을 내기 때문에 개수가 적음)
            else:
                finalFreqList.append(freqList[(index1+index2)/2])#peak와 그 다음 peak의 평균 위치의 frequency를 추가

    rawLengthList = []
    for index in range(len(peakList)-1):
        rawLengthList.append(peakList[index+1]-peakList[index])#peak끼리의 간격을 계산하여 raw Length를 저장
    unitLength = float(min(rawLengthList)) * 1.25 # 간격중 가장 작은 것의 1.25배를 unit length로 설정(1.25배를 해주는 이유는 간격이 작게 설정될 경우 발생하는 오차가 증폭되기 때문)

    unitLengthList = []
    for length in rawLengthList:
        unitLengthList.append(round(length/unitLength))#길이를 unit length로 나누어준 후 round를 취함
    unitLengthList.append(round((len(wavFileModifier.wavArray)-peakList[-1])/unitLength))
    
    returnList = []
    for index in range(len(peakList)):
        temp = []
        temp.append(finalFreqList[index])# 각원소에 freq 데이터 추가
        if int(unitLengthList[index]) == 0: temp.append(1)# round를 취한 값이 0일 경우 길이를 1로 설정
        else: temp.append(int(unitLengthList[index]))#각 원소에 음 길이 추
        returnList.append(temp)
    return returnList
