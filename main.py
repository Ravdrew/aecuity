import pyo as p
import random as r

f = open("presets.txt", "a")

directionValues = (-90, 90)  # left, right
numToDirection = ("left", "right")
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

s = p.Server(duplex=1, buffersize=1024, winhost='asio',nchnls=2)
s.setInputDevice(1)  # USER DEPENDENT
s.setOutputDevice(4)

s.boot()
w = open("presets.txt", "w")
# Drops the gain by 20 dB.
s.amp = 0.4

while True:
    selectedSound = r.randrange(0, 22, 1)  # selects sound to be played
    direction = r.randrange(0, 2, 1)
    degreeModifier = r.randrange(-10, 10)

    soundPlayer = p.SfPlayer(sounds[selectedSound], loop=False)
    chBinaural = p.HRTF(soundPlayer, azimuth=directionValues[direction] + degreeModifier)
    print(directionValues[direction] + degreeModifier)

    mixer = p.Mixer(outs=2,chnls=2)
    mixer.addInput(0,chBinaural)
    mixer.setAmp(0,0,0.9)
    mixer.setAmp(0,1,0.9)
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

