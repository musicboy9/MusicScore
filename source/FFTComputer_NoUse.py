import matplotlib.pyplot as plt
from scipy.io import wavfile # get the api
from scipy.fftpack import fft

class FFTComputer:
    
    def __init__(self):
        self.frequency = 0.0
        self.amplitude = 0.0
    
    def computeFFT(self,wavfile):
        a = wavfile.T[0] # this is a two channel soundtrack, I get the first track
        b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
        c = fft(b) # calculate fourier transform (complex numbers list)
        plt.plot(abs(c),'r')    
        
    