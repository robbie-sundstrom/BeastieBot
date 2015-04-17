from Tkinter import *
from subprocess_test import *

class BeastieInterface:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        #Quit Button
        self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
        self.button.grid(row=0,column=0,sticky=W)
        
        #Welcome Button
        self.slogan = Button(frame,
                         text="Welcome",
                         command=self.write_slogan)
        self.slogan.grid(row=0,column=1)
        
        #Record Button
        self.audio = Button(frame,
                         text="Record Rap",
                         command=self.record)
        self.audio.grid(row=0,column=2)
        
        #Play Butoon
        self.play = Button(frame,
                         text="Play Rap",
                         command=self.play)
        self.play.grid(row=1,column=2)

        self.return_theme = Button(frame,
                         text="Enter",
                         command=self.fetch)
        self.return_theme.grid(row=2, column=2)        
        
    
        self.v = StringVar()
        self.entry_label = Label(frame,
        	             text="Inspirative Word:")
        self.entry_label.grid(row=2,column=0)

        self.entry = Entry(frame,
                         textvariable=self.v)
        self.entry.grid(row=2,column=1)
    
    def write_slogan(self):
        print "Welcome to Beastie Bot! Enter an inspirative word and get ready to spit some hot fire."

    def record(self):
        arecord()

    def play(self):
    	aplay()
    
    def set_theme(self):
    	return self.v.get()
    
    def fetch(self):
        print self.v.get()

root = Tk()
app = BeastieInterface(root)
root.mainloop()