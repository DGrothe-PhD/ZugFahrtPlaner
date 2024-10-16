#!/usr/bin/python3
import os


class TrainTicket:
    '''Reads and gathers the relevant data from a Deutsche Bahn train ticket.
    Input: Text file containing the raw text from a printable PDF ticket.
    For PDFs run ExtractText first.
    Generates an HTML file and a short summary text file.
    The summary text file can be read by any synthetic reader.
    We recommend py3-tts here, see the enclosed example.py.
    Or you can copy this in an email to your friend. Happy holidays and have fun!
    
    Params:
        filename - the filename of the raw text file. Ending .txt is automatically added.
        
    '''
    inputFilePrefix = "demo_Bahntickettext"
    # Strings to be recognized
    def clearing(self):
        """initialization, text parts for filtering"""
        self.startDateIntro = "Ihre Reiseverbindung und Reservierung Hinfahrt am"
        self.signsOfTravelData = ["Barcode bitte nicht knicken!", "Zangenabdruck",
         "Halt Datum Zeit Gleis"]
        self.endDateIntro = "Ihre Reiseverbindung und Reservierung Rückfahrt am"
        #
        # Extracted travel data
        self.paymentInfo = []
        self.startTravelDate = ""
        self.endTravelDate = ""
        self.travelToString = ""
        self.travelersmessage = ""
        self.zugInfo= []

    def __init__(self, n=-1, filename = "demo_Bahntickettext" ):
        """Main processing"""
        self.clearing()
        self.inputFilePrefix = filename
        numAsString = str(n) if n >=0 else ""
        self.fullFileName = self.inputFilePrefix + numAsString + ".txt"
        timefound = False
        with open(self.fullFileName, "r", encoding="utf_8") as inputfile:
            for line in inputfile:
                # Preis und Zahlung
                if "Zahlung" in line or "€" in line or line.startswith("Betrag"):
                    self.paymentInfo.append("<p>" +line.strip() + "</p>")
                # Anfang der Reisedaten
                if line.startswith(tuple( self.signsOfTravelData)):
                    timefound = True
                    continue
                #
                if line.startswith(self.startDateIntro):
                    timefound = True
                # Ende der Reisedaten
                if line.startswith(("Wichtige Nutzungshinweise:", "amtlichem Lichtbildausweis")):
                    self.zugInfo.append("</p>")
                    break
                if line.startswith("Nichtraucher") or line.strip() in {"Hinfahrt:", "Rückfahrt:"}:
                    continue
                #
                if not timefound:
                    continue
                if line.startswith(self.startDateIntro):
                    self.startTravelDate = line[len(self.startDateIntro):].strip()
                    self.travelToString += f"\r\nMeine Hinfahrt ist am {self.startTravelDate}:\r\n"
                    self.zugInfo.append(f"<p><b>Hinfahrt am {self.startTravelDate}:</b><br>")
                elif line.startswith(self.endDateIntro):
                    self.endTravelDate = line[len(self.endDateIntro):].strip()
                    self.travelToString += f"\r\nMeine Rückfahrt ist am {self.endTravelDate}:\r\n"
                    self.zugInfo.append("</p>")
                    self.zugInfo.append(f"<p><b>Rückfahrt am {self.endTravelDate}:</b><br>")
                else:
                    text = line.strip(',\r\n \t')
                    if ". a" in text:
                        self.gatherTimeAndPlace(text)
                        text = text.replace(". a",".&nbsp;&nbsp;<b>a") + "</b>"
                    else:
                        if "IC" in text:
                            self.addTrainNumberAndPlace(text)
                    text+= "<br>"
                    self.zugInfo.append(text)
        #
        ofilename = "TicketDaten_" + self.inputFilePrefix + numAsString + ".html"
        with open(ofilename, "w", encoding="utf_8") as outputfile:
            outputfile.write("<!DOCTYPE html><html lang=\"de\"><head>" + \
             "<meta charset=\"utf-8\">"+os.linesep)
            outputfile.write(f"<title>Reise von {self.startTravelDate} bis "+ \
             f"{self.endTravelDate}</title></head><body>"+os.linesep)
            outputfile.write(os.linesep.join(self.paymentInfo))
            outputfile.write(os.linesep)
            outputfile.write(os.linesep.join(self.zugInfo))
            outputfile.write(os.linesep + "</body></html>")
        outputfile.close()
        #
        self.generateSpeakableText()
        self.writeTextFile(numAsString)

    def clarify(self, text):
        """Un-abbreviate stuff."""
        s = text.replace("Wg.", "Wagen")
        s = s.replace("Pl.", "Sitzplatz")
        s = s.replace("ICE", "I C E")
        s = s.replace("Hbf", "Hauptbahnhof")
        return s

    def generateSpeakableText(self):
        """Generate a full-sentence text with the main info."""
        self.travelersmessage = "Hallo, ich werde vom "
        self.travelersmessage += self.startTravelDate
        self.travelersmessage += " bis zum " + self.endTravelDate + \
        " eine Bahnreise unternehmen.\r\n Details:\r\n"
        self.travelersmessage += self.travelToString

    def writeTextFile(self, numAsString):
        """write speakable text to a plain text file"""
        textfile = f"Reiseplan_{self.inputFilePrefix}{numAsString}.txt"
        with open(textfile, "w", encoding="utf_8") as tfile:
            tfile.write(self.travelersmessage + "\r\n")
        tfile.close()

    def addTrainNumberAndPlace(self, text):
        """Add train number and seat number"""
        self.travelToString += f"Und zwar habe ich im {self.clarify(text)} gebucht.\r\n"

    def gatherTimeAndPlace(self, text):
        """gather timetable details"""
        if "ab" in text:
            text = "Start " + self.clarify(text)
        else:
            text = "Ziel " + self.clarify(text)
        snippets = text.split(" ")
        #
        for q in snippets:
            if ":" in q:
                self.travelToString += q + " Uhr "
            elif len(q.strip()) > 2:
                self.travelToString += q.strip() + " "
            elif q.startswith("a"):
                self.travelToString += q.strip() + " "
            else:
                self.travelToString += "vom Gleis "+q.strip()
        self.travelToString += "\r\n"