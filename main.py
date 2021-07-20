import pyo as p
import random as r
import sys

f = open("presets.txt", "a")

directionValues = (-90, 90, -45, 45, -135, 135)  # left, right, front left, front right, back left, back right
numToDirection = ("l", "r", "fl", "fr", "bl", "br")
sounds = ("plasticNoises.wav", "decafCoffeeMonoFinal.wav", "dogBark.wav", "pianoA.wav", "pianoB.wav", "pianoC.wav",
          "pianoD.wav", "pianoE.wav", "pianoF.wav", "pianoG.wav", "sinkRunning.wav", "showerRunning.wav",
          "gettingHome.wav", "longTimeNoSee.wav", "Hertz250.wav", "Hertz500.wav", "Hertz1000.wav", "Hertz2000.wav", "Hertz4000.wav",
          "Hertz6000.wav", "roomba.wav", "cars.wav")

with open("presets.txt", "r") as reader:  # opens file reader to pull saved score
    output = reader.readline()

if output != "":
    score = int(output)
else:
    score = 0
print(f"Previous Score: {score}")

s = p.Server(duplex=1, buffersize=1024, winhost='asio', nchnls=2)
s.setInputDevice(1)  # USER DEPENDENT
s.setOutputDevice(4)

s.boot()
w = open("presets.txt", "w")

s.amp = 0.45

print("Modes:")
print("0: Training Mode")
print("1: Not training mode \n")
mode = int(input("Please chose a mode: "))

while True:
    if mode == 1:
        selectedSound = r.randrange(0, 22, 1)  # selects sound to be played
        direction = r.randrange(0, 6, 1)
        degreeModifier = 0 # r.randrange(-10, 10)

        soundPlayer = p.SfPlayer(sounds[selectedSound], loop=False)
        chBinaural = p.HRTF(soundPlayer, azimuth=directionValues[direction])
        print(directionValues[direction])

        noiseVolume = 0.005 + score*0.001
        if noiseVolume > 0.07:
            noiseVolume = 0.07

        noise = p.BrownNoise(noiseVolume).mix(2).out()
        mixer = p.Mixer(outs=2, chnls=2)
        mixer.addInput(0, chBinaural)
        mixer.setAmp(0, 0, 0.9)
        mixer.setAmp(0, 1, 0.9)
        mixer.out()
        s.start()

        guess = input("What direction is the sound coming from? (l/r/fl/fr/bl/br/save): ")
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
            break
        else:  # handles wrong answer
            print("\nAh, sorry, try again!")
            print(f"Your score was {score}! Nice job!\n")
            s.stop()
            break
    elif mode == 0:
        possible_inputs = ['l', 'r', 'fl', 'fr', 'bl', 'br']
        direction = input("Type in l/r/fl/fr/bl/br to select which direction you would like to practice, or q to quit: ")
        if direction in possible_inputs:
            soundPlayer = p.SfPlayer(sounds[15], loop=True) 
            chBinaural = p.HRTF(soundPlayer, azimuth=directionValues[numToDirection.index(direction)])
        elif direction.lower() == "q":
            continue
        else:
            print("Invalid input: Try again")

sys.exit()

