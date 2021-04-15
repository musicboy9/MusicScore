#-*-coding:utf-8-*-
# ===================================
# Date : 2016-06-01 start
# Made by 농구인생
# visualize해주는 GUI 구현
# ===================================

from Tkinter import *
from tkMessageBox import *
import os
from time import *
from convertToLilypond import *
from FFTMANUAL import *


class akbobada(Frame):
    
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title('악보받아')
        
        self.tc = Frame(self)
        self.tc.grid(row = 0, column = 0)
        
        self.c = Frame(self)
        self.c.grid(row = 1, column = 0)
        
        self.titlecanvas = Canvas(self.tc, width = 400, height = 100)
        self.titlecanvas.grid(row = 0, column = 0, rowspan = 5)
        
        self.mainmenu = Canvas(self.c, width = 400, height = 200)
        self.mainmenu.grid(row = 0, column = 0, rowspan = 2, columnspan = 3)     
        
        self.blankLabel = Label(self.tc)
        self.blankLabel.grid(row = 0, column = 0)
        
        self.title = PhotoImage(file = 'akbobada.gif')
        self.titleLabel = Label(self.tc, image = self.title)
        self.titleLabel.grid(row = 1, column = 0, rowspan = 4)
    
        self.wavefile_txtLabel = Label(self.c, text = '   MUSIC START!')
        self.wavefile_txtLabel.grid(row = 0, column = 0, sticky = E)
        
        self.wavefile = StringVar()
        self.wavefileEntry = Entry(self.c, justify = 'center', width = 15, textvariable = self.wavefile)
        self.wavefileEntry.grid(row = 0, column = 1, sticky = E)
        
        self.wav_txtLabel = Label(self.c, text = '.wav')
        self.wav_txtLabel.grid(row = 0, column = 2, sticky = W)
        
        
        
        self.startButton = Button(self.c, text = 'Let\'s make a score!',command = self.option)
        self.startButton.grid(row = 1, column = 0, columnspan = 3, sticky = N)
        
        
        self.developer = Label(self.c, text = 'Made by 농구인생     \n   ')
        self.developer.grid(row = 1, column = 1, columnspan = 2, sticky = S + E)
        
    def option(self):
        
        path = os.getcwd() + '\\' + self.wavefile.get() + '.wav'
        
        if not os.path.exists(path):
            showerror(message = 'Error : File does not exist!', parent = self)
            return
        
        def drawScore():
            if options.title.get() == '':
                if askyesno('Warning!','Is it OK to be an empty title?'): pass
                else: return
            
            title = '\"' + options.title.get() + '\"'
        
            time = time_txt.get()
            time = time[:time.index("|")-1] + '/' + time[time.index("|") + 2:]
            
            
            instrument = '\"' + options.instrument.get() + '\"'
            
            
            # fft 통해 melodylist 만들기
            
            convertToLilypondFile(noteGenerator(self.wavefile.get()), title, time, instrument)
            sleep(1)
            showinfo( 'Finish', 'pdf built complete!')
            options.destroy()
                
        options = Toplevel(self)
        options.title('Option')
        
        options.canvas = Canvas(options, width = 600, height = 160)
        options.canvas.grid(row = 0, column = 0, rowspan = 6, columnspan = 3)
        
        options.title_txt = Label(options, text = 'Title ')
        options.title_txt.grid(row = 1, column = 0, sticky = E)
        
        options.title = StringVar()
        options.titleEntry = Entry(options, justify = 'center' , width = 10, textvariable =options.title)
        options.titleEntry.grid(row = 1, column = 1)
        
        
        
        
        options.time_txt = Label(options, text = ' Time ')
        options.time_txt.grid(row = 2, column = 0, sticky = E)
        
        # 옵션박스 생성~~
        time_txt = StringVar(options)
        time_txt.set('4 | 4')
        
        options.time = OptionMenu(options, time_txt, '4 | 4', '2 | 4', '3 | 4', '2 | 2', '3 | 8', '6 | 8', '12 | 8')
        options.time.pack()
        options.time.grid(row = 2, column = 1)
        
        
        
        options.instrument_txt = Label(options, text = 'Instrument ')
        options.instrument_txt.grid(row = 3, column = 0, sticky = E)
        
        options.instrument = StringVar()
        options.instrument.set('Piano')
        options.instrumentEntry = Entry(options, justify = 'center' , width = 10, textvariable =options.instrument)
        options.instrumentEntry.grid(row = 3, column = 1)        
                
                
        options.scoreExample = PhotoImage(file = 'score_eg.gif')
        options.scoreExLabel = Label(options, image = options.scoreExample)
        options.scoreExLabel.grid(row = 1, column = 2, rowspan = 3)
        
        
        options.drawButton = Button(options, text = ' Draw ', command = drawScore)
        options.drawButton.grid(row = 4, column = 2, sticky = S + W)
        
        options.backButton = Button(options, text = ' Back ', command = options.destroy)
        options.backButton.grid(row = 4, column = 2, sticky = S)  
        

        
        
            
    
def main(): akbobada().mainloop()

main()
    
        
        
        