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

        #Quit Button
        self.button = Button(frame, 
                         text="QUIT", fg="red",
                         command=frame.quit)
        self.button.grid(row=0,column=2,sticky=E)

        #Text Entry and Label
        self.entry_label = Label(frame,
                         text="Inspirative Word:")
        self.entry_label.grid(row=0,column=0, sticky=W)

        self.entry = Entry(frame,
                         textvariable=self.word,
                         width=10)
        self.entry.grid(row=0,column=1, sticky =W)

        #Number Entry and Label
        self.entry_label = Label(frame,
                         text="Number of Lines:")
        self.entry_label.grid(row=1,column=0, sticky=W)

        self.entry = Entry(frame,
                         textvariable=self.lines,
                         width=10)
        self.entry.grid(row=1,column=1,sticky=W)

        #Enter Button 
        self.return_theme = Button(frame,
                         text="Enter",
                         command=self.fetch1)
        self.return_theme.grid(row=2, column=1, sticky=W)
        
        #Profanity Checkbox
        self.profanity = Checkbutton(frame,
                         text="Clean",
                         variable = self.censored)
        self.profanity.select() # clean by default
        self.profanity.grid(row=1, column=2, sticky=W)

        #Rap Text
        self.rap_text = Text(frame, width=40)
        self.rap_text.grid(row = 4, columnspan=3)

    def fetch1(self):
        rhymelist = find_rhymes(self.word.get())
        self.fetch2(rhymelist, 0, int(self.lines.get()))

    def fetch2(self, rhymelist, currentrhyme, linelimit):
        if currentrhyme == 4:
            combostart()    # start the music and recording
        if currentrhyme >= len(rhymelist):
            self.rap_text.insert(END, '.\n.\n.\nNo more rhymes left!\n')
            return None
        if currentrhyme >= linelimit:
            self.rap_text.insert(END, '.\n.\n.\nBeastieBot OUT\n')
            return None

        thistweet = find_tweet(rhymelist[currentrhyme], 2, self.censored.get())
        if thistweet == "":    # if it doesn't find a tweet
            # make sure we still get the same number of lines
            root.after(1,self.fetch2,rhymelist,currentrhyme+1,linelimit+1)
        else:
            try:
                print 'found tweet'
                self.rap_text.insert(END, thistweet+'\n')
                self.rap_text.update_idletasks()
                root.after(1,self.fetch2,rhymelist,currentrhyme+1,linelimit)
            # except UnicodeEncodeError:
            except TclError:
                # if there's an emoticon, skip this one
                print 'Tcl Error man'
                root.after(1,self.fetch2,rhymelist,currentrhyme+1,linelimit+1)

root = Tk()
app = BeastieInterface(root)
root.mainloop()