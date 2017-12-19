import os
import rospy
from std_msgs.msg import String
from pocketsphinx import LiveSpeech, get_model_path, Decoder
import pyaudio
import time

drinks_list = ["Paradise", "Martini", "Rose", "Manhattan", "Screwdriver", "Gibson", "Bacardi", "Americano"]
caps_drinks_list = []
for item in drinks_list:
	caps_drinks_list.append(item.upper())


def listen(MODE):
    CORPUS = 6278
    model_path = get_model_path()
    home_path = "/home/the0s/Desktop/HCR_Python"
    print(model_path)
    print(home_path)
    DATADIR = "/usr/local/lib/python2.7/dist-packages/pocketsphinx/data"

    config = Decoder.default_config()
    config.set_string('-hmm', os.path.join(model_path, 'hub4wsj_sc_8k'))
    config.set_string('-lm', os.path.join(home_path, str(CORPUS)+'.lm.bin'))
    config.set_string('-dict', os.path.join(home_path, str(CORPUS)+'.dic'))
    config.set_string('-logfn', '/dev/null')
    decoder = Decoder(config)

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    in_speech_bf = False
    decoder.start_utt()
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
            if decoder.get_in_speech() != in_speech_bf:
                    in_speech_bf = decoder.get_in_speech()
                    if not in_speech_bf:
                            decoder.end_utt()
                            if decoder.hyp() is not None:
				buf = [s for s in decoder.hyp().hypstr.split()]
                                print(buf)
				if len(buf) > 0:
		                        if MODE == 0: #DrinkRequest
						for item in buf:
							if checkRequest(item) != "NONE":
								output = checkRequest(item)		
								stream.stop_stream()
								stream.close()
								return output
		                        if MODE == 1: #DrinkConfirm
						for item in buf:
							if checkConfirm(item) != "NONE":
								output = checkConfirm(item)		
								stream.stop_stream()
								stream.close()
								return output
	
                            decoder.start_utt()
        else:
            break
    decoder.end_utt()

def checkRequest(phrase):
	global caps_drinks_list
	global drinks_list
	if phrase in caps_drinks_list:
		index = caps_drinks_list.index(phrase)
		return (drinks_list[index])
	else:
		return("NONE")


def checkConfirm(phrase):
	if phrase == "YES":
		return("YESS")
	elif phrase == "NO":
		return ("NOO")
	else:
		return("NONE")

pub = rospy.Publisher('drinks_listener', String, queue_size=1)
rospy.init_node('drinks_listener', anonymous=True)
rate = rospy.Rate(10)	

def callback(data):
	if data.data == "request":
		print("Looking for drink name")
		patron_speech = listen(0)
		print("Patron:",patron_speech)
    		pub.publish(patron_speech)
	
	elif data.data == "confirm":
		print("Looking for confirmation")
		patron_speech = listen(1)
		print("Patron:",patron_speech)
    		pub.publish(patron_speech)
	

sub = rospy.Subscriber('drinks_listener', String, callback)

while not rospy.is_shutdown():
    time.sleep(1)


