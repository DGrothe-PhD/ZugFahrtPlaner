#!/usr/bin/python
import re
from PyPDF2 import PdfReader
from PyPDF2 import errors

class extractText:
    """
    For desktop usage on Windows or Linux
    Extracts text from a given PDF file.
    Output file: PlainTextContent.txt
    
    User input:
     - name of an existing PDF file including its ending
     - or: exit to quit this program.
    
    After one PDF file has successfully been processed,
    the program quits automatically.
    
    
    Exceptions:
     - PdfReadError if no readable PDF or reading error occurred
     - Exception if PDF not found or anything else went wrong
    """
    plainTextContentFile = "./PlainTextContent.txt"
    #
    def __init__(self):
        """interactive PDF extractor"""
        print("PDF-Textkonverter. \nZum vorzeitigen Beenden tippen Sie 'exit'.")
        while True:
            self.pdfPlainText = ""
            self.myPDFpath = input("Type a PDF file name:")
            # easy step out
            if self.myPDFpath.endswith("exit"):
                print("Programm wird beendet.")
                break
            if not self.myPDFpath.endswith(".pdf"):
                print("Kein PDF-Dateiname eingegeben.")
                continue
            try:
                with PdfReader(open(self.myPDFpath, "rb")) as self.myPDF:
                    self.processPDF()
                break
                #
            except errors.PdfReadError as exP:
                print(f"{self.myPDFpath} konnte nicht gelesen werden.")
                print(f"Genaue Fehlermeldung: {exP}")
            except Exception as whatwrong:
                print(f"{self.myPDFpath} ist nicht aufrufbar. Bitte prüfen Sie Ihre Eingabe!")
                print(f"Genaue Fehlermeldung: {whatwrong}")

    # to be extended in the future
    # Need extra linebreak after platform number
    def clarify(self, txt):
        """clean stuff"""
        x = re.sub(r'(\d)(ICE)', r'\1\n\2', txt)
        return x

    def processPDF(self):
        """initialize page list"""
        #pagelist = []
        #firstit=True
        ln = '\n'#os.linesep
        # grab all text from PDF per page and put into page list
        with open(self.plainTextContentFile, "w", encoding="utf_8") as fobjVb:
            for p, pdfpage in enumerate(self.myPDF.pages):
                self.pdfPlainText = pdfpage.extract_text()
                fobjVb.write(f"{ln}{ln}-- Seite {p+1} --{ln}")
                self.pdfPlainText = self.clarify(self.pdfPlainText)
                fobjVb.write(self.pdfPlainText)
        fobjVb.close()
