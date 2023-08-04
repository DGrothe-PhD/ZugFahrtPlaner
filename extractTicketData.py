#!/usr/bin/python3
import os

class TrainTicket:
    '''Reads and gathers the relevant data from a Deutsche Bahn train ticket.
    Input: Text file containing the raw text from a printable PDF ticket.
    For PDFs run ExtractText first.
    Generates an HTML file and a short summary text file.
    The text of the summary text file can be read by any synthetic reader.
    Or you can copy this in an email to your friend. Happy holidays and have fun!
    
    Params:
        filename - the filename of the raw text file. Ending .txt is automatically added.
        
    '''
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
        self.TravelToString = ""
        self.travelersmessage = ""
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
                    self.TravelToString += f"\r\nMeine Hinfahrt ist am {self.startTravelDate}:\r\n"
                    self.zugInfo.append(f"<p><b>Hinfahrt am {self.startTravelDate}:</b><br>")
                elif line.startswith(self.endDateIntro):
                    self.endTravelDate = line[len(self.endDateIntro):].strip()
                    self.TravelToString += f"\r\nMeine Rückfahrt ist am {self.endTravelDate}:\r\n"
                    self.zugInfo.append("</p>")
                    self.zugInfo.append(f"<p><b>Rückfahrt am {self.endTravelDate}:</b><br>")
                else:
                    text = line.strip(',\r\n \t')
                    if text.__contains__(". a"):
                        self.gatherTimeAndPlace(text)
                        text = text.replace(". a",".&nbsp;&nbsp;<b>a") + "</b>"
                    else:
                        if text.__contains__("IC"):
                            self.AddTrainNumberAndPlace(text)
                    text+= "<br>"
                    self.zugInfo.append(text)
        self.SpeakableText()
        ofilename = "TicketDaten_" + self.inputFilePrefix + number_as_string + ".html"
        outputfile = open(ofilename, "w", encoding="utf_8")
        outputfile.write("<!DOCTYPE html><html lang=\"de\"><head><meta charset=\"utf-8\">"+os.linesep)
        outputfile.write(f"<title>Reise von {self.startTravelDate} bis {self.endTravelDate}</title></head><body>"+os.linesep)
        outputfile.write(os.linesep.join(self.paymentInfo))
        outputfile.write(os.linesep)
        outputfile.write(os.linesep.join(self.zugInfo))
        outputfile.write(os.linesep + "</body></html>")
        outputfile.close()
        #
        textfile = "Reiseplan_" + self.inputFilePrefix + number_as_string + ".txt"
        tfile = open(textfile, "w", encoding="utf_8")
        tfile.write(self.travelersmessage + "\r\n")
        tfile.close()
    
    def clarify(self, text):
        s = text.replace("Wg.", "Wagen")
        s = s.replace("Pl.", "Sitzplatz")
        s = s.replace("ICE", "I C E")
        s = s.replace("Hbf", "Hauptbahnhof")
        return s
        
    def SpeakableText(self):
        self.travelersmessage = "Hallo, ich werde vom "
        self.travelersmessage += self.startTravelDate
        self.travelersmessage += " bis zum " + self.endTravelDate + " eine Bahnreise unternehmen.\r\n Details:\r\n"
        self.travelersmessage += self.TravelToString
    def AddTrainNumberAndPlace(self, text):
        self.TravelToString += "Und zwar habe ich im " + self.clarify(text) + " gebucht.\r\n"
    
    def gatherTimeAndPlace(self, text):
        if text.__contains__("ab"):
            text = "Start " + self.clarify(text)
        else:
            text = "Ziel " + self.clarify(text)
        snippets = text.split(" ")
        for q in snippets:
            if q.__contains__(":"):
                self.TravelToString += q + " Uhr "
            elif len(q.strip()) > 2:
                self.TravelToString += q.strip() + " "
            elif q.startswith("a"):
                self.TravelToString += q.strip() + " "
            else:
                self.TravelToString += "vom Gleis "+q.strip()
        self.TravelToString += "\r\n"