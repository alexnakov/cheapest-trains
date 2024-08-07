import os

file = "not-sound-1.wav"
print('playing sound using native player')
os.system("afplay " + file)