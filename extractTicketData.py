#!/usr/bin/python3
import os

class TrainTicket:
    inputFilePrefix = "demo_Bahntickettext"
    # Strings to be recognized
    def clearing(self):
        self.startDateIntro = "Ihre Reiseverbindung und Reservierung Hinfahrt am"
        self.signsOfTravelData = ["Barcode bitte nicht knicken!", "Zangenabdruck",
         "Halt Datum Zeit Gleis"]
        self.endDateIntro = "Ihre Reiseverbindung und Reservierung Rückfahrt am"
    
        # Extracted travel data
        self.paymentInfo = []
        self.startTravelDate = ""
        self.endTravelDate = ""
        self.zugInfo= []
    
    def __init__(self, n=-1, filename = "demo_Bahntickettext" ):
        self.clearing()
        self.inputFilePrefix = filename
        number_as_string= str(n) if n >=0 else ""
        self.fullFileName = self.inputFilePrefix + number_as_string + ".txt"
        timefound = False
        with open(self.fullFileName, "r", encoding="utf_8") as inputfile:
            for line in inputfile:
                # Preis und Zahlung
                if line.__contains__("Zahlung") or line.__contains__("€") or line.startswith("Betrag"):
                    self.paymentInfo.append("<p>" +line.strip() + "</p>")
                # Anfang der Reisedaten
                if line.startswith(tuple( self.signsOfTravelData)):
                    timefound = True
                    continue
                elif line.startswith(self.startDateIntro):
                    timefound = True
                # Ende der Reisedaten
                if line.startswith("Wichtige Nutzungshinweise:") or line.startswith("amtlichem Lichtbildausweis"):
                    self.zugInfo.append("</p>")
                    break
                if line.startswith("Nichtraucher"): continue
                if line.strip() == "Hinfahrt:" or line.strip() == "Rückfahrt:": continue
                #
                if not timefound:
                    continue
                if line.startswith(self.startDateIntro):
                    self.startTravelDate = line[len(self.startDateIntro):].strip()
                    self.zugInfo.append(f"<p><b>Hinfahrt am {self.startTravelDate}:</b><br>")
                elif line.startswith(self.endDateIntro):
                    self.endTravelDate = line[len(self.endDateIntro):].strip()
                    self.zugInfo.append("</p>")
                    self.zugInfo.append(f"<p><b>Rückfahrt am {self.endTravelDate}:</b><br>")
                else:
                    text = line.strip(',\r\n \t')
                    if text.__contains__(". a"):
                        text = text.replace(". a",".&nbsp;&nbsp;<b>a") + "</b>"
                    text+= "<br>"
                    self.zugInfo.append(text)
        
        ofilename = "TicketDaten_" + self.inputFilePrefix + number_as_string + ".html"
        outputfile = open(ofilename, "w", encoding="utf_8")
        outputfile.write("<!DOCTYPE html><html lang=\"de\"><head><meta charset=\"utf-8\">"+os.linesep)
        outputfile.write(f"<title>Reise von {self.startTravelDate} bis {self.endTravelDate}</title></head><body>"+os.linesep)
        outputfile.write(os.linesep.join(self.paymentInfo))
        outputfile.write(os.linesep)
        outputfile.write(os.linesep.join(self.zugInfo))
        outputfile.write(os.linesep + "</body></html>")
        outputfile.close()
