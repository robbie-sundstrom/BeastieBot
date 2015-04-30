"""script that pulls together separate working components into user interface. 
"""
from Tkinter import *
from BeastieAudio import *
from BeastieBot2 import *
from subproc_combo import *

class BeastieInterface:
    "Only class, meant to create UI box"
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        self.word = StringVar() #Input Word
        self.lines = StringVar() #Input Number of Lines
        self.explicitness = IntVar() 

        #Quit Button
        self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
        self.button.grid(row=0,column=0,sticky=W)
        
        # #Welcome Button
        # self.slogan = Button(frame,
        #                  text="Welcome",
        #                  command=self.write_slogan)
        # self.slogan.grid(row=0,column=1)
        
        #Record Button
        self.audio = Button(frame,
                         text="Record Rap",
                         command=self.record)
        self.audio.grid(row=0,column=3, sticky=E)
        
        #Play Butoon
        self.play = Button(frame,
                         text="Play Rap",
                         command=self.play_rap)
        self.play.grid(row=0,column=2, sticky=E)

        #Text Entry and Label
        self.entry_label = Label(frame,
        	             text="Inspirative Word:")
        self.entry_label.grid(row=2,column=0, sticky=W)

        self.entry = Entry(frame,
                         textvariable=self.word)
        self.entry.grid(row=2,column=1, sticky =W)

        #Number Entry and Label
        self.entry_label = Label(frame,
        	             text="Number of Lines:")
        self.entry_label.grid(row=3,column=0, sticky=W)

        self.entry = Entry(frame,
                         textvariable=self.lines)
        self.entry.grid(row=3,column=1,sticky=W)

        #Enter Button 
        self.return_theme = Button(frame,
                         text="Enter",
                         command=self.fetch)
        self.return_theme.grid(row=4, column=1, sticky=E)        
        
        #Profanity Checkbox
        self.profanity = Checkbutton(frame,
                         text="Clean",
                         variable = self.explicitness)
        self.profanity.grid(row=3, column=3, sticky=W)

        #Rap Text
        self.rap_text = Text(frame)
        self.rap_text.grid(row = 6, columnspan=4)


    def write_slogan(self):
        print "Welcome to Beastie Bot! Enter an inspirative word and get ready to spit some hot fire."

    def record(self):
        combo_record()

    def play_rap(self):
    	play()
        
    def fetch(self):
        self.rap_text.insert(INSERT, beastie_it_up(self.word.get(), int(self.lines.get())))

    def addTweet(self, tweet):
        self.rap_text.insert(END, tweet)

# class Rap(lines):
#     lines = lines
#     beastie_it_up(self.word.get(), int(self.lines.get()))
#     for line in rap:
#         print line 

root = Tk()
app = BeastieInterface(root)
root.mainloop()
