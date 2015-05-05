import subprocess, threading, time 
"""record and play audio at same time"""

def play():
	a2='aplay background.wav'
	subprocess.call(a2, shell=True)

def record():
	a1="arecord -d 60 rap.wav"
	subprocess.call(a1, shell=True)

def combo1():
	threading.Thread(target=record).start()

def combo2():
	threading.Thread(target=play).start()

def combostart():
	threading.Thread(target=combo1).start()
	threading.Thread(target=combo2).start()