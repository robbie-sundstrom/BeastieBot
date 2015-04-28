import subprocess, threading, time 
"""record and play audio at same time, use threading to accomplish both"""

def play():
	a2='aplay intergallactic.wav'
	subprocess.call(a2, shell=True)

def record():
	a1="arecord -d 10 rap.wav"
	subprocess.call(a1, shell=True)

def combo1():
	"handle threading for recording"
	while time.time() <= start_time:
		pass
	threading.Thread(target=record).start()

def combo2():
	"handle threading for playing"
	while time.time()<=start_time:
		pass
	threading.Thread(target=play).start()
start_time =time.time()+20
threading.Thread(target=combo1).start()
threading.Thread(target=combo2).start()


