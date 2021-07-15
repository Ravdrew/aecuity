import pyo as p
import os
import time
import random as r

# setup

directionValues = ((0.9, 0.1), (0.1, 0.9)) # left[left, right], right[left, right]
numToDirection = ("left", "right")
sounds = ("recording1.wav", "recording2.wav", "recording3.wav")

# set score
with open("presets.txt", "r") as reader:
    output = reader.readline()

print(f"output: {output}")
if output != "":
    score = int(output)
else:
    score = 0
print(f"score: {score}")
# set score

s = p.Server(duplex=1, buffersize=1024, winhost='asio',nchnls=2)
s.setInputDevice(1)
s.setOutputDevice(4)
s.boot()


# setup
w = open("presets.txt", "w")

while True:
    selectedSound = r.randrange(0, 3, 1)
    direction = r.randrange(0, 2, 1) # not inclusive, stops at 1
    modifier = r.uniform(0, 0.1) # 0.2??

    soundLeft = p.SfPlayer(sounds[selectedSound],loop=False)
    soundRight = p.SfPlayer(sounds[selectedSound],loop=False)

    mixer = p.Mixer(outs=2,chnls=1)
    mixer.addInput(voice=0, input=soundLeft)
    mixer.addInput(voice=1, input=soundRight)

    # print(f"sound: {selectedSound}")
    if direction == 0:
        # print(f"direct: {direction}")
        # print(f"modif: {modifier}")
        mixer.setAmp(vin=0,vout=0,amp=directionValues[direction][0] - modifier)
        mixer.setAmp(vin=1,vout=1,amp=directionValues[direction][1] + modifier)
    if direction == 1:
        # print(direction)
        # print(modifier)
        mixer.setAmp(vin=0,vout=0,amp=directionValues[direction][0] + modifier)
        mixer.setAmp(vin=1,vout=1,amp=directionValues[direction][1] - modifier)
    mixer.out()

    s.start()

    guess = input("What direction is the sound coming from? (left/right/save): ")
    if guess.lower() == numToDirection[direction]:
        score += 1
        print("\nCongratulations! You are correct!")
        print(f"Your score is: {score}\n")
        s.stop()
        continue
    elif guess.lower() == "save":
        print("Saving your score, good work!")
        print(f"Your saved score was: {score}\n")
        print("See you!")
        w.write(str(score))
        w.close()
        s.stop()
        exit()
    else:
        print("\nAh, sorry, try again!")
        print(f"Your score was {score}! Nice job!\n")
        exit()

