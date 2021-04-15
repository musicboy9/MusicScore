#-*-coding:utf-8-*-
# ================================================
# Date : 2016-05-26 started
# Made by 농구인생
# FFT를 통해 얻은 박자와 진동수를 가지고 Lilypond에
# import 가능한 형태의 text file을 만들어주는 code
# ================================================

import math
import os
import copy
from time import *
from majortest import *

mislist = ['c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'b']
meslist = ['c', 'des', 'd', 'ees', 'e', 'f', 'ges', 'g',' aes', 'a', 'bes', 'b']
flist = [[441,4.0], [440,4.0], [880,4.0], [880,4.0], [441,4.0], [440,4.0], [880,4], [880,4], [441,4], [440,4], [880,4], [880,4], [441,4], [440,4], [880,4], [880,4], [441,4], [440,4], [880,4], [880,4], [441,4], [440,4], [880,4], [880,4], [441,4], [440,4], [880,4], [880,4], [441,4], [440,4], [880,4], [880,4], [441,4], [440,4], [880,4], [880,4.0]]

fl = [[440, 3], [440,1]]


# fft를 통해 각 음의 길이와 주파수 구해져있음
# 각각의 freq, 음의 길이는 tuple 형태로 저장

def frequencyToMelody(freq, mlist):
    temp = math.log(freq / 261.63 * 2, 2) * 12
    i = round(temp)
    octave, melody = i / 12, int(i % 12)
    return int(octave), mlist[melody]



def chooseLength(fftList, l, time):
    fftlist = copy.deepcopy(fftList)
    cnt = 0
    numer = time[:time.index("/") ]
    denom = time[time.index("/") + 1 :]    
    for i in range(len(fftlist)):
        fftlist[i][1] = float(l) / fftlist[i][1] * fftList[0][1]
        
        if fftlist[i][1] < 0.9 : return False
        if int(numer) < int(denom) / float(fftlist[i][1]): return False
        cnt +=  int(denom) / float(fftlist[i][1])
        fftlist[i][1] = round(fftlist[i][1],2)
        
    
        
    if cnt%int(numer) != 0: return False
    return fftlist


def fftlistToMelodylist(fftList, mlist):
    melodyList = []
    for i in fftList:
        oct, mel = frequencyToMelody(i[0], mlist)
        if oct > 0:
            for cnt in range(oct):
                mel += '\''
        else:
            for cnt in range((-1)*oct):
                mel += ','
        
        if abs(i[1] - 1) <= 0.1 : i[1] = 1
        elif abs(i[1] - 1.33) <= 0.1 : i[1] = '2.'
        elif abs(i[1] - 2) <= 0.1: i[1] = 2
        elif abs(i[1] - 4) <= 0.1 : i[1] = 4
        elif abs(i[1] - 8) <= 0.1 : i[1] = 8
        elif abs(i[1] - 16) <= 0.1 : i[1] = 16
        
        mel += str(i[1])
        melodyList.append(mel)
        
    return melodyList

    
def convertToLilypondFile(fftList, title, time, instrument):
    for l in [1, 4/3.0, 2, 4, 8]:
        flist = chooseLength(fftList, l, time)
        if flist:
            key = majortest(fftList)
            if key in ['c', 'g', 'd', 'a', 'e', 'b', 'fis', 'cis']: mlist = mislist
            else : mlist = meslist
            key = key + ' \\major'
            melodyList = fftlistToMelodylist(flist, mlist)
            score_str = ''
            for i in melodyList: score_str += i + ' '
            script = "\\header{title = %s} \n\nstaff = \\new Staff{{\n    \\key %s \n    \\set Staff.instrumentName = %s \n    \\time %s \n\n    %s \n    \\bar \"|.\"\n    }\n}\n\n\\score{\n    \\staff\n}"%(title, key, instrument, time, score_str)
            f = open("TEMP.ly", 'w')
            f.write(script)
            f.close()
            os.startfile("TEMP.ly")
            sleep(3)
            os.rename("TEMP.pdf", title[1:-1] + "_" + str(round(l,2)) + ".pdf")

