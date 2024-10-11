#!/usr/bin/python3

import pyttsx3 as tts
from extractTicketData import TrainTicket
#from ExtractText import ExtractText

#for i in range(1,11):
#	foo = TrainTicket(i)

#textquelle = ExtractText()
#
tickettmp = TrainTicket(7)

speaker = tts.init()
speaker.say(tickettmp.travelersmessage)
speaker.runAndWait()