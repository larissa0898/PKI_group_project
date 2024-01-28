# Bildbearbeitungstool (Gruppe A1-1)
Dieses Projekt ist ein Bildbearbeitungstool, das eine Vielzahl von Funktionen für Bildmanipulation, Effekte und Erkennung bietet.

#### Inhaltsverzeichnis
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Funktionen](#funktionen)
- [Daten](#daten)
- [Literatur](#literatur)

## Installation
Um das Bildbearbeitungstool lokal zu installieren und auszuführen, müssen die folgenden Schritte ausgeführt werden:
1. **Tesseract OCR installieren:**
   Zunächst sollte Tesseract unter ```C:\Program Files\Tesseract-OCR\tesseract.exe``` installiert sein. Wenn dies nicht der Fall ist, kann Tesseract [hier](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe) heruntergeladen werden. Die Installation für MacOS und Linux kann [hier](https://tesseract-ocr.github.io/tessdoc/Installation.html) nachgelesen werden. 
   Bei der Installation unbedingt beachten, dass bei der Komponentenauswahl ein Haken bei *Additional language data* gesetzt wird.

3. **Klonen des Repositories**
   ```bash
   git clone https://github.com/larissa0898/PKI_group_project.git
   cd PKI_group_project
   ```

4. **Optionale Erstellung und Aktivierung einer virtuellen Umgebung:**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # Unter Windows: myenv\Scripts\activate
   ```

5. **Installation der erforderlichen Pakete:**
   ```bash
   pip install -r requirements.txt
   ```

## Verwendung
Nach der Installation des Projekts kann das Bildbearbeitungstool aus dem Verzeichnis "./PKI_group_project/" gestartet werden:
```bash
python main.py
```

## Funktionen

- **Standardeffekte:** Enthält grundlegende Bildbearbeitungswerkzeuge wie Rotieren, Skalieren, Spiegeln usw.
  
- **Erweiterte Effekte:** Bietet erweiterte Effekte wie Markup, Blur Effekt, Filter usw.

- **Objekt- und Gesichtserkennung:** Ermöglicht die Erkennung von Objekten und Gesichtern in Bildern. *Hinweis: Die Gesichtswiedererkennung ist aktuell nur mit Bildern von Elon Musk möglich.*

- **OCR (Optical Character Recognition):** Ermöglicht die Erkennung und Extraktion von Text aus Bildern. Aktuell sind folgende Sprachen verfügbar: Deutsch, Englisch, Französisch, Spanisch und Italienisch.


## Daten
- YOLO - Fehlende yolov3.weights von: https://github.com/patrick013/Object-Detection---Yolov3/blob/master/model/yolov3.weights

- Bilder von Claus-Peter Koch und Dietmar Ysop  

## Literatur
Youtube zu Tesseract OCR - https://www.youtube.com/watch?v=6DjFscX4I_c


