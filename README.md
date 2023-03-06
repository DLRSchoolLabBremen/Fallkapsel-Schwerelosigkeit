# Fallkapsel
Für die Fallkapsel benötigt man...

## Setup/Installatsion
Für die Fallkapsel muss der Mikrokontroller eingerichtet werden und das live-Graph programm auf einem Rechner installiert werden.

### Live-Graph
Der live-Graph ist ein python basiertes skript, dass ausgeführt wird.
Um dieses auf einem Rechner einzurichten müssen folgende Schritte ausgeführt werden:
1. Speichere den gesamten Ordner Fallkapsel_Programm an einen geünschten Ort
2. Installiere Python (3.9.7)
   - Auf Windows geht dies über den [Microsoft Store](https://apps.microsoft.com/store/detail/python-39/9P7QFQMJRFP7)
3. Dependecides Installieren
   - öffne die Konsole (in der Windowssuchleiste nach "cmd" suchen und "Eingabeaufforderung" ausführen)
   - Öffne den Dateipfad des Programms:
     - ```cd /mein/pfad/zum/ordner/Fallkapsel_Programm ```
   - ```pip install -r requirements.txt```
4. Porgramm ausführen
   - Führe die ersten zwei Schritte aus 3. aus
   - Um das Programm zu starten gebe in die Konsoloe:
     - ```python bt_server_fallkapsel.py ```
