# ZugFahrtPlaner
extract relevant info for planning train trips. Minimal formatted, as HTML and text file. Readable content both for use in an email to your friends or facilitate automatic reading.

## Wie es funktioniert
In einem ersten Schritt wird mit `ExtractText` der Rohtext aus einer vorhandenen PDF-Onlineticket der Deutschen Bahn in eine Textdatei geschrieben.

Nun kann die `TrainTicket`-Klasse den Rohtext des Zugtickets verarbeiten. 

Die Ausgabe enthält dann alle und nur die relevanten Infos wie Wagennummer und Gleis(e), um Mitfahrer z. B. per Mail über die Fahrzeiten zu informieren.
Ausgabe als
* minimal formatierte HTML 
* Fließtext optimiert für digitale Vorlesefunktionen.
* Python kann dann vorzugsweise gleich selbst den Text vorlesen (Windows-Schnittstelle)
