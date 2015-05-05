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

#### Paste API Keys Here ####
apidict = {0: TwitterSearch(
                consumer_key = 'PASTE HERE',
                consumer_secret = 'PASTE HERE',
                access_token = 'PASTE HERE',
                access_token_secret = 'PASTE HERE')}

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
              in; 1 means censored and 0 means not censored
    returns: a string of the tweet, or an empty string if no tweet is
             found
    """
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([sourceword]) # word to search for
    tso.set_language('en') # English tweets only
    tso.set_include_entities(False) # don't give us entity information

    ts = apidict[0]

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
            elapsed = time.time() - start
    except TwitterSearchException:
        print ('All api keys have reach their rate limit. Please try again'
               'in 15 minutes.')
        sys.exit(0)

    # if no tweet is found, return a blank string
    return ""

class BeastieInterface:
    def __init__(self, master):
        #Create a Tkinter frame
        frame = Frame(master)
        frame.pack()
        
        self.word = StringVar() #Input Word
        self.lines = StringVar() #Input Number of Lines
        self.censored = IntVar() #Input Whether Censored or Not

        #Quit Button
        self.button = Button(frame, 
                             text="QUIT", fg="red",
                             command=frame.quit)
        self.button.grid(row=0, column=2, sticky=E)

        #Text Entry
        self.entry_label = Label(frame,
                                 text="Inspirative Word:")
        self.entry_label.grid(row=0, column=0, sticky=W)

        self.entry = Entry(frame,
                           textvariable=self.word,
                           width=10)
        self.entry.grid(row=0, column=1, sticky =W)

        #Number of Lines Entry
        self.entry_label = Label(frame,
                                 text="Number of Lines:")
        self.entry_label.grid(row=1, column=0, sticky=W)

        self.entry = Entry(frame,
                           textvariable=self.lines,
                           width=10)
        self.entry.grid(row=1, column=1, sticky=W)

        #Enter Button 
        self.return_theme = Button(frame,
                                   text="Enter",
                                   command=self.start)
        self.return_theme.grid(row=2, column=1, sticky=W)
        
        #Profanity Checkbox
        self.profanity = Checkbutton(frame,
                                     text="Clean",
                                     variable = self.censored)
        self.profanity.select() #Clean by default
        self.profanity.grid(row=1, column=2, sticky=W)

        #Text box where rap shows up
        self.rap_text = Text(frame, width=40)
        self.rap_text.grid(row=4, columnspan=3)

    def start(self):
        """
        This is the function called when the user presses the enter button.
        Gets a list of rhymes, and then calls beastie_it_up with a
        currentrhyme of 0.

        returns: None
        """
        #Find rhymes for the input word:
        rhymelist = find_rhymes(self.word.get())
        #Beasite up the rhymelist:
        self.beastie_it_up(rhymelist, 0, int(self.lines.get()))

    def beastie_it_up(self, rhymelist, currentrhyme, linelimit):
        """
        Recursively finds tweets ending in each rhyme in rhymelist, and prints
        them to the GUI line-by-line as they are found.  Keeps going until it
        reaches the linelimit, or if there are no more rhymes left.

        rhymelist: the list of rhymes to find tweets from
        currentrhyme: the index of the rhyme that this function should find
                      a tweet for, used for recursive purposes
        linelimit: the total number of lines to print
        returns: None
        """

        #Start the music and recording after the 4th rhyme:
        if currentrhyme == 4:
            combostart()
 
        # If we run out of rhymes:
        if currentrhyme >= len(rhymelist):
            self.rap_text.insert(END, '.\n.\n.\nNo more rhymes left!\n')
            return None

        # If we finish:
        if currentrhyme >= linelimit:
            self.rap_text.insert(END, '.\n.\n.\nBeastieBot OUT\n')
            return None

        # Find tweet for the current rhyme, search for 2 seconds
        thistweet = find_tweet(rhymelist[currentrhyme],
                               2,
                               self.censored.get())

        # If it doesn't find a tweet:
        if thistweet == "":
            # Call this function again using the next rhyme,
            # increase the limit because this rhyme doesn't count
            root.after(1,
                       self.beastie_it_up,
                       rhymelist,
                       currentrhyme + 1,
                       linelimit + 1)
        else:
            try:
                # Insert this tweet at the end of the GUI text box
                # and update it:
                self.rap_text.insert(END, thistweet + '\n')
                self.rap_text.update_idletasks()
                # Call this function again with the next rhyme:
                root.after(1,
                           self.beastie_it_up,
                           rhymelist,
                           currentrhyme + 1,
                           linelimit)
            except TclError:
                # If there's an emoticon, we get a TclError, so we have to
                # skip this rhyme and go to the next one, increasing the
                # limit because this rhyme doesn't count
                root.after(1,
                           self.beastie_it_up,
                           rhymelist,
                           currentrhyme + 1,
                           linelimit + 1)

root = Tk()
app = BeastieInterface(root)
root.mainloop()