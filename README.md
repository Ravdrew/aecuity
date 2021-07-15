# aecuity
COSMOS Cluster 5 Research Project - Training Hearing Impaired

**Important Instructions:** 
If you're getting an error that says something like **"Portaudio"...** then you need to change your audio input and output device on lines 25 and 26.

To do so:
1. In another python file with pyo run function: **pa_list_devices()**
2. Locate your input and output device in the printed list and mark down their indexes
3. Open the main.py file in this program and change the number in functions **s.setInputDevice(1)** and **s.setOutputDevice(4)** to reflect your input and output device indexes
4. Run code and enjoy!
