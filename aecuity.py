import pyo as p
import random as r
import sys

f = open("presets.txt", "a")

boldOpen = "\033[1m"
boldClose = "\033[0m"

directionValues = (-90, 90, -140, 140, 0)  # left, right, front left, front right, back left, back right
numToDirection = ("l", "r", "bl", "br", "f")
numToFullString = ("LEFT", "RIGHT", "BACK LEFT", "BACK RIGHT", "FRONT")
sounds = ("sounds/plasticNoises.wav", "sounds/decafCoffeeMonoFinal.wav", "sounds/dogBark.wav", "sounds/pianoA.wav",
          "sounds/pianoB.wav", "sounds/pianoC.wav", "sounds/pianoD.wav", "sounds/pianoE.wav", "sounds/pianoF.wav",
          "sounds/pianoG.wav", "sounds/sinkRunning.wav", "sounds/showerRunning.wav", "sounds/new_longtime.wav",
          "sounds/overhere.wav", "sounds/Hertz250.wav", "sounds/Hertz500.wav", "sounds/Hertz1000.wav",
          "sounds/Hertz2000.wav", "sounds/Hertz4000.wav", "sounds/Hertz6000.wav", "sounds/roomba.wav", "sounds/cars.wav",
          "sounds/paperCrumple.wav", "sounds/windPaper.wav", "sounds/knocking.wav", "sounds/clapping.wav",
          "sounds/DroppingBooksonWood.wav", "sounds/HelloThereAllison.wav", "sounds/sister-002.wav", "sounds/driving.wav",
          "sounds/honk.wav")
count = 0

with open("presets.txt", "r") as reader:  # opens file reader to pull saved score
    output = reader.readline()

if output != "":
    score = int(output)
else:
    score = 0

s = p.Server(duplex=1, buffersize=1024, winhost='asio', nchnls=2)
s.setInputDevice(1)  # USER DEPENDENT
s.setOutputDevice(4)

s.boot()
w = open("presets.txt", "w")

s.amp = 0.45

print("\nSelect a Mode:")
print("0: Training Mode")
print("1: Scoring Mode \n")
mode = int(input("Please chose a mode: "))

while True:
    if mode == 1:
        selectedSound = r.randrange(0, 31, 1)  # selects sound to be played
        direction = r.randrange(0, 5, 1)
        degreeModifier = 0  # r.randrange(-10, 10)

        soundPlayer = p.SfPlayer(sounds[selectedSound], loop=False)
        if direction == 2 or direction == 3:
            # print("lowpass")
            lowpassFil = p.Tone(soundPlayer, 1880)
            chBinaural = p.HRTF(lowpassFil, azimuth=directionValues[direction])
        else:
            # print("no lowpass")
            chBinaural = p.HRTF(soundPlayer, azimuth=directionValues[direction])
        # print(directionValues[direction])

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

        guess = input("What direction is the sound coming from? (l/r/bl/br/f/save): ")
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
            s.shutdown()
            break
        else:  # handles wrong answer
            print("\nAh, sorry, the direction was: ")
            print(boldOpen + numToFullString[direction] + boldClose)
            print(f"Your score was {score}! Nice job!\n")
            s.stop()
            s.shutdown()
            break
    elif mode == 0:
        userDirection = input("Type in l/r/bl/br/f to select which direction you would like to practice, or q to quit: ")
        if count > 0:  # stops pyo warning
            s.stop()
        if userDirection in numToDirection:
            count += 1
            userSoundPlayer = p.SfPlayer(sounds[1], loop=True)
            if numToDirection.index(userDirection) == 2 or numToDirection.index(userDirection) == 3:
                userlowpassFil = p.Tone(userSoundPlayer, 1880)
                userChBinaural = p.HRTF(userlowpassFil, azimuth=directionValues[numToDirection.index(userDirection)])
            else:
                userChBinaural = p.HRTF(userSoundPlayer, azimuth=directionValues[numToDirection.index(userDirection)])
            userMixer = p.Mixer(outs=2, chnls=2)
            userMixer.addInput(0, userChBinaural)
            userMixer.setAmp(0, 0, 0.9)
            userMixer.setAmp(0, 1, 0.9)
            userMixer.out()
            s.start()
        elif userDirection.lower() == "q":
            sys.exit()
        else:
            print("Invalid input: Try again")

sys.exit()
