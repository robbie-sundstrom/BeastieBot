import subprocess 
"""uses subprocess to record the rap in a wav format
"""
a1="arecord -d 10 rap.wav" #terminal command to be passed in


subprocess.call(a1, shell=True)