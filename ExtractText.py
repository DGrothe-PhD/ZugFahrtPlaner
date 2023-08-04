#!/usr/bin/python
import os
import re
from PyPDF2 import PdfReader

myPDFpath = './DBExampleTicket.pdf'


myPDF = PdfReader(open(myPDFpath, "rb"))

#Need extra linebreak after platform number
def clarify(txt):
    x = re.sub(r'(\d)(ICE)', r'\1\n\2', txt)
    return x

# initialize page list
pagelist = []
firstit=True
ln = '\n'#os.linesep
# grab all text from PDF per page and put into page list    
with open("./DBExampleTicket.txt", "w", encoding="utf_8") as fobj_vb:
    for page in range(0, len(myPDF.pages)):
        currentPage = myPDF.pages[page]
        myText = currentPage.extract_text()
        fobj_vb.write(f"{ln}{ln}-- Seite {page+1} --{ln}")
        myText = clarify(myText)
        fobj_vb.write(myText)
fobj_vb.close()
