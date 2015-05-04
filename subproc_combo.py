import subprocess, threading, time 
"""record and play audio at same time"""

def play():
	a2='aplay mannythedog.wav'
	subprocess.call(a2, shell=True)

def record():
	a1="arecord -d 120 rap.wav"
	subprocess.call(a1, shell=True)

def combo1():
	# while time.time() <= start_time:
		# pass
	threading.Thread(target=record).start()

def combo2():
	# while time.time()<=start_time:
		# pass
	threading.Thread(target=play).start()
# start_time =time.time()+20

def combostart():
	# start_time = time.time()+10
	# while time.time() < start_time:
	# 	pass
	threading.Thread(target=combo1).start()
	threading.Thread(target=combo2).start()


#if __name__ == '__main__':
#	combo()