import pyo as p
import os
import time
import random as r

f = open("presets.txt", "a")

# setup

directionValues = ((0.85, 0.15), (0.15, 0.85))  # left[left, right], right[left, right]
numToDirection = ("left", "right")
sounds = ("recording1.wav", "decafCoffeeMonoFinal.wav", "recording3.wav")

# set score

with open("presets.txt", "r") as reader:  # opens file reader to pull saved score
    output = reader.readline()

if output != "":
    score = int(output)
else:
    score = 0
print(f"Previous Score: {score}")
# set score

s = p.Server(duplex=1, buffersize=1024, winhost='asio',nchnls=2)  # settings for pyo server
s.setInputDevice(1)  # USER DEPENDENT
s.setOutputDevice(4)  # USER DEPENDENT
s.boot()


# setup
w = open("presets.txt", "w")  # opens file writer to save score

while True:
    selectedSound = r.randrange(0, 3, 1)  # selects sound to be played
    direction = r.randrange(0, 2, 1)  # selects direction
    modifier = r.uniform(0, 0.125)  # adds a little bit of variety in where the sound comes from

    soundLeft = p.SfPlayer(sounds[selectedSound], loop=False)  # sets selected sound to be played
    soundRight = p.SfPlayer(sounds[selectedSound], loop=False)

    noiseVolume = 0.005 + score*0.001
    if noiseVolume > 0.07:
        noiseVolume = 0.07

    difficultyVolume = score*0.01
    if difficultyVolume > 0.1:
        difficultyVolume = 0.1

    noise = p.BrownNoise(noiseVolume).mix(2).out()
    mixer = p.Mixer(outs=2, chnls=1)  # sets 2 outputs
    mixer.addInput(voice=0, input=soundLeft)
    mixer.addInput(voice=1, input=soundRight)

    if direction == 0:  # sets volume for each side depending on direction
        mixer.setAmp(vin=0,vout=0,amp=directionValues[direction][0] - modifier - difficultyVolume)
        mixer.setAmp(vin=1,vout=1,amp=directionValues[direction][1] + modifier + difficultyVolume)
        print(directionValues[direction][1] + modifier + difficultyVolume)
    if direction == 1:
        mixer.setAmp(vin=0,vout=0,amp=directionValues[direction][0] + modifier + difficultyVolume)
        print(directionValues[direction][0] + modifier + difficultyVolume)
        mixer.setAmp(vin=1,vout=1,amp=directionValues[direction][1] - modifier - difficultyVolume)
    mixer.out()
    s.start()

    guess = input("What direction is the sound coming from? (left/right/save): ")
    if guess.lower() == numToDirection[direction]:  # checks if correct
        score += 1
        print("\nCongratulations! You are correct!")
        print(f"Your score is: {score}\n")
        s.stop()
        continue
    elif guess.lower() == "save":  # handles save option
        print("Saving your score, good work!")
        print(f"Your saved score was: {score}\n")
        print("See you!")
        w.write(str(score))
        w.close()
        s.stop()
        exit()
    else:  # handles wrong answer
        print("\nAh, sorry, try again!")
        print(f"Your score was {score}! Nice job!\n")
        exit()

