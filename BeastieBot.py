"""
THE FINAL CODE

Created Apr 5, 2015

@authors Mackenzie Frackleton, Emily Mamula, Robert Siegel, Bill Wong
"""
from TwitterSearch import *
from profanity_list import bad_words
from profanity import profanity
profanity.load_words(bad_words)
from countsyl import count_syllables
from Tkinter import *
# from BeastieAudio import *
# from BeastieBot2 import *
from subproc_combo import *
import time, urllib2, json, random, sys

apinum = 0
apis_done = 0
filter_on = True
#### PUT apidict HERE ####

def find_rhymes(sourceword):
    """
    Generates a list of perfect rhymes of the sourceword, sorted by
    frequency in the English language.

    sourceword: the word to find rhymes of
    returns: A list of perfect rhymes
    """
    url = "http://rhymebrain.com/talk?function=getRhymes&word=" + sourceword
    f = urllib2.urlopen(url)
    rawrhymes = f.read()

    rhymes_dicts_list = json.loads(rawrhymes)

    perfect_rhymes_dicts_list = []

    for diction in rhymes_dicts_list:
        if diction['score'] >= 300:
            perfect_rhymes_dicts_list.append(diction)
    sorted_list = sorted(perfect_rhymes_dicts_list, key=lambda k: k['freq'],
                         reverse=True)

    wordlist = []
    for diction in sorted_list:
        wordlist.append(str(diction['word']))
    return wordlist

def find_tweet(sourceword, timelimit, censored):
    """
    Searches Twitter for a tweet ending in the sourceword. Only
    searches for tweets between 5 and 10 syllables long. Ignores
    tweets with '@' symbols or links to avoid retweets and unnecessary
    syllables.

    If no tweet is found before the timelimit, returns a blank string.

    sourceword: word that the tweets should end with
    timelimit: maximum number of seconds to search for
    censored: an integer respresenting whether to censor the tweets that come
              in or not; 1 means censored and 0 means not censored
    returns: a string of the tweet, or an empty string if no tweet is
             found
    """
    global apinum, apis_done
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([sourceword]) # word to search for
    tso.set_language('en') # English tweets only
    tso.set_include_entities(False) # don't give us entity information

    ts = apidict[apinum]

    start = time.time()
    elapsed = 0

    try:
        for tweet in ts.search_tweets_iterable(tso):
            if elapsed >= timelimit:
                break

            thistweet = tweet['text']
            sylcount = count_syllables(thistweet)

            # check for ending word
            if (thistweet[-(len(sourceword)):] == sourceword or
                thistweet[-(len(sourceword)+1):] == sourceword+'.'):
                # check syllables, '@' symbols, and links
                if (sylcount <= 10 and sylcount >= 5 and
                    '@' not in thistweet and 'http' not in thistweet):
                    # profanity filter
                    if censored == 0:   # if it's not censored
                        return thistweet
                    if not profanity.contains_profanity(thistweet):
                        # if there's no profanity, then return thistweet
                        return thistweet
                    print "PROFANE TWEET:",thistweet
            elapsed = time.time() - start
    except TwitterSearchException:
        apinum = (apinum + 1) % 3
        apis_done += 1
        if apis_done >= 3:  # if we exhausted all api keys
            print ('All api keys have reach their rate limit. Please '
                   'try again in 15 minutes.')
            sys.exit(0)
        return find_tweet(sourceword, timelimit,censored)

    return ""

class BeastieInterface:
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        
        self.word = StringVar() #Input Word
        self.lines = StringVar() #Input Number of Lines
        self.censored = IntVar() 

        #Rap Text
        self.rap_text = Text(frame)
        # self.rap_text = Canvas(frame, width=200, height=100)
        self.rap_text.grid(row = 6, columnspan=4)

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
                         command=self.fetch1)
        self.return_theme.grid(row=4, column=1, sticky=E)
        
        #Profanity Checkbox
        self.profanity = Checkbutton(frame,
                         text="Clean",
                         variable = self.censored)
        self.profanity.grid(row=3, column=3, sticky=W)

    def write_slogan(self):
        print "Welcome to Beastie Bot! Enter an inspirative word and"\
                "get ready to spit some hot fire."

    def record(self):
        combo_record()

    def play_rap(self):
        play()

    def fetch1(self):
        rhymelist = find_rhymes(self.word.get())
        self.fetch2(rhymelist, 0, int(self.lines.get()))

    def fetch2(self, rhymelist, currentrhyme, linelimit):

        # while i < linelimit and i < len(rhymelist):

        # print 'adding oh yeah'
        # self.rap_text.insert(END, 'oh yeah\n')
        # self.rap_text.update_idletasks()
        # root.after(300, self.fetch2)

        if currentrhyme >= linelimit or currentrhyme >= len(rhymelist):
            self.rap_text.insert(END, '.\n.\n.\nBeastieBot OUT\n')
            return None

        thistweet = find_tweet(rhymelist[currentrhyme], 2, self.censored.get())
        if thistweet == "":    # if it doesn't find a tweet
            # make sure we still get the same number of lines
            root.after(1,self.fetch2,rhymelist,currentrhyme+1,linelimit+1)
        else:
            try:
                # print thistweet
                #TODO: change this to display on gui
                # self.addTweet(thistweet)
                print 'found tweet'
                self.rap_text.insert(END, thistweet+'\n')
                self.rap_text.update_idletasks()
                root.after(1,self.fetch2,rhymelist,currentrhyme+1,linelimit)
            except UnicodeEncodeError:
                # if there's an emoticon, skip this one
                root.after(1,self.fetch2,rhymelist,currentrhyme+1,linelimit+1)
        
    def fetch(self):
        # self.rap_text.insert(INSERT, beastie_it_up(self.word.get(), int(self.lines.get())))
        # self.beastie_it_up(self.word.get(), int(self.lines.get()))
        # root.after(1000, self.addTweet, 'tweet man')
        # for i in range(4):
            # root.after(i*1000, self.addTweet, 'tweet man')
            # self.rap_text.insert(END, 'poop\n')
            # time.sleep(1)
        rhymelist = find_rhymes(self.word.get())
        linelimit = int(self.lines.get())

        i = 0
        while i < linelimit and i < len(rhymelist):
            thistweet = find_tweet(rhymelist[i], 2, self.censored.get())
            if thistweet == "":    # if it doesn't find a tweet
                # make sure we still get the same number of lines
                linelimit += 1
            else:
                try:
                    # print thistweet
                    #TODO: change this to display on gui
                    # self.addTweet(thistweet)
                    print 'found tweet'
                    root.after(1, self.addTweet, thistweet)
                    self.rap_text.update_idletasks()
                except UnicodeEncodeError:
                    linelimit += 1 # if there's an emoticon, skip this one
            i += 1

    def addTweet(self, tweet):
        print 'adding tweet dude'
        print 'censored:',self.censored.get()
        self.rap_text.insert(END, tweet+'\n')

    def beastie_it_up_2(self, rhyme):
        """

        rhymelist: the list of rhymes to iterate through
        rhymenumber: the index of the current rhyme we're on
        returns: None
        """
        thistweet = find_tweet(rhyme, 2, self.censored.get())
        if thistweet == "":    # if it doesn't find a tweet
            # make sure we still get the same number of lines
            linelimit += 1
        else:
            try:
                # print thistweet
                #TODO: change this to display on gui
                # self.addTweet(thistweet)
                # self.rap_text.update_idletasks()
                root.after(1, self.addTweet, thistweet)
            except UnicodeEncodeError:
                linelimit += 1 # if there's an emoticon, skip this one


    def beastie_it_up(self, sourceword, linelimit):
        """
        Prints tweets that end in a words that rhyme with the sourceword.
        Prints each tweet as it finds it. Stops after linelimit tweets, or
        after there are no more rhymes.

        sourceword: the word to rhyme with
        linelimit: the maximum number of lines to print
        returns: None
        """
        rhymelist = find_rhymes(sourceword)
        # print rhymelist
        start = time.time()
        elapsed = 0

        i = 0
        while i < linelimit and i < len(rhymelist):
            thisword = rhymelist[i]
            thistweet = find_tweet(thisword, 2, self.censored.get())
            if thistweet == "":    # if it doesn't find a tweet
                # make sure we still get the same number of lines
                linelimit += 1
            else:
                try:
                    # print thistweet
                    #TODO: change this to display on gui
                    # self.addTweet(thistweet)
                    # self.rap_text.update_idletasks()
                    root.after(1, self.addTweet, thistweet)
                except UnicodeEncodeError:
                    linelimit += 1 # if there's an emoticon, skip this one
            i += 1

root = Tk()
app = BeastieInterface(root)
root.mainloop()