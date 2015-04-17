import subprocess

def arecord():
	a1 = "arecord -d 10 rap.wav"
	subprocess.call(a1, shell=True)

def aplay():
	a2 = "aplay rap.wav"
	subprocess.call(a2, shell=True)
