#!/usr/bin/python3

import pyttsx3 as tts
from extractTicketData import TrainTicket

#pylint: disable=W0718
#from ExtractText import ExtractText

#for i in range(1,11):
#	foo = TrainTicket(i)

#textquelle = ExtractText()
#
tickettmp = TrainTicket(7)

try:
    speaker = tts.init()
    speaker.say(tickettmp.travelersmessage)
    speaker.runAndWait()
except KeyboardInterrupt:
    pass
except:
    print("TTS error occurred")
#pylint: enable=W0718