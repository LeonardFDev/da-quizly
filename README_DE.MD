# Quizly

[🇬🇧 English version](README.MD)

## Beschreibung

Dieses Projekt wurde als Lernprojekt entwickelt, um die Entwicklung einer Webanwendung mit Django und dem Django REST Framework praxisnah zu erlernen. Im Fokus steht die Umsetzung eines Backends mit einer REST API, über die ein bereitgestelltes Frontend mit dem Backend kommuniziert. Dabei werden unter anderem HTTP-Anfragen verarbeitet und geschützte Endpunkte mithilfe einer JWT-basierten Authentifizierung abgesichert. Hierfür werden Access- und Refresh-Tokens verwendet, die über Cookies zwischen Frontend und Backend übertragen und verwaltet werden.

Darüber hinaus wird eine Audiodatei heruntergeladen und lokal verarbeitet. Die Audiodatei wird zunächst mithilfe einer Speech-to-Text-Anwendung in Text transkribiert. Der daraus entstandene Text wird anschließend zusammen mit einem definierten Prompt an eine KI übergeben. Die von der KI generierte Antwort wird daraufhin vom Backend weiterverarbeitet und für die weitere Verwendung aufbereitet.

---

## Quickstart

### 1. Repository klonen

```bash
git clone https://github.com/LeonardFDev/da-quizly.git .
```

### 2. Virtuelle Umgebung erstellen und aktivieren 

#### Erstellen:

```bash
python -m venv env
```

#### Aktivieren:

Windows CMD:

```bash
"env/Scripts/activate" 
```

Windows PowerShell:

```bash
.\env\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source ./env/bin/activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. .env
Eine `.env`-Datei erstellen und den `GEMINI_API_KEY` eintragen.

### 5. Datenbank vorbereiten

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### 6. Superuser erstellen (optional)

```bash
python manage.py createsuperuser
```

### 7. Entwicklungsserver starten

```bash
python manage.py runserver
```

---

# Features

* Django REST API
* JWT-basierte Authentifizierung mit Access- und Refresh-Tokens
* Audiodatei-Download
* Speech-to-Text-Transkription
* KI-gestützte Textverarbeitung

---

# Technologien

| Technologie           | Version                        |
| --------------------- | ------------------------------ |
| Python                | 3.13.3                         |
| Django                | 6.1.1                          |
| Django REST Framework | 3.18.1                         |
| Django Cors Headers   | 4.9.0                          |
| Imageio ffmpeg        | 0.6.0                          |
| Python dotenv         | 1.2.3                          |
| yt-dlp                | 2026.8.19                      |
| openai-whisper        | 20250625                       |
| google-genai          | 2.25.0                         |
| Datenbank             | SQLite3                        |
| Authentifizierung     | JWT-basierte Authentifizierung |

---

# Voraussetzungen

Folgende Software wird benötigt:

* Python 3.13.3 oder höher
* pip
* Git

Das Projekt wurde unter Windows entwickelt.

Da es sich um eine Django Web API handelt, sollte die Anwendung grundsätzlich auch unter anderen Betriebssystemen mit Python-Unterstützung lauffähig sein.

Mögliche Betriebssysteme:

* Windows
* Linux
* macOS

---

# FFmpeg

Das Problem mit FFmpeg sollte grundsätzlich bereits im Code behoben sein. Sollte FFmpeg dennoch Probleme verursachen, kann es manuell installiert und eingerichtet werden.

## Windows
### Option 1: Installation per Download

1. Lade ein aktuelles FFmpeg-Build herunter:

    * [FFmpeg – Download](https://ffmpeg.org/download.html)

    * Für Windows werden häufig Builds von [gyan.dev](<https://www.gyan.dev/ffmpeg/builds/>) oder [BtbN](<https://github.com/BtbN/FFmpeg-Builds/releases>) verwendet.

2. Entpacke die ZIP-Datei, z. B. nach:

```Text
C:\ffmpeg
```


3. Öffne den Ordner `bin`. Dort befindet sich die Datei `ffmpeg.exe`.

4. Füge den `bin`-Ordner zu den Windows-Umgebungsvariablen hinzu:

    * Rechtsklick auf „Dieser PC“ → „Eigenschaften“

    * „Erweiterte Systemeinstellungen“ öffnen

    * „Umgebungsvariablen…“ auswählen

    * Unter „Path“ den folgenden Eintrag ergänzen:

```Text
C:\ffmpeg\bin
```

### Option 2: Installation über das Terminal

Alternativ kann FFmpeg direkt über winget installiert werden:

```powershell
winget install --id Gyan.FFmpeg -e --source winget
```

## macOS

Unter macOS ist die Installation über [Homebrew](https://brew.sh/) am einfachsten.

Falls Homebrew noch nicht installiert ist, führe folgenden Befehl im Terminal aus:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Anschließend FFmpeg installieren:

```bash
brew install ffmpeg
```

---

# Django Apps

Das Projekt verwendet folgende Django Apps:

| App                   | Beschreibung                                                                                          |
| --------------------- | ----------------------------------------------------------------------------------------------------- |
| `auth_app`            | Stellt API-Endpunkte für Registrierung, Anmeldung, Abmeldung und token refresh bereit.                |
| `quiz_management_app` | Stellt API-Endpunkte für Quiz und Question bereit.                                                    |

Zusätzlich werden folgende Django-Komponenten verwendet:

* `rest_framework`
* `rest_framework_simplejwt`
* `rest_framework_simplejwt.token_blacklist`

---

# Datenbank

Das Projekt verwendet die von Django standardmäßig unterstützte SQLite-Datenbank.

SQLite wird verwendet, da das Projekt als Lernprojekt entwickelt wird und aktuell keine Anforderungen an eine externe oder produktionsorientierte Datenbank bestehen.

Die Datenbank wird lokal über folgende Datei verwaltet:

```text
db.sqlite3
```

---

# Migrationen

Migrationen verwalten Änderungen an der Datenbankstruktur.

Aktueller Stand:

* Es existieren aktuell keine eigenen Datenbankmigrationen.

Sobald Django Models erstellt oder verändert werden, müssen Migrationen erzeugt werden.

Neue Migration erstellen:

```bash
python manage.py makemigrations
```

Migrationen anwenden:

```bash
python manage.py migrate
```

---

# Superuser erstellen

Für den Zugriff auf das Django Admin Interface kann ein Administrator erstellt werden:

```bash
python manage.py createsuperuser
```

Danach ist der Admin-Bereich erreichbar unter:

```text
admin/
```

---

# Entwicklungsserver starten

Der lokale Entwicklungsserver wird gestartet mit:

```bash
python manage.py runserver
```

Standardmäßig ist die Anwendung erreichbar unter:

```text
http://127.0.0.1:8000/
```

---

# Authentifizierung

Die API verwendet eine JWT-basierte Authentifizierung über das Django REST Framework. Für die Authentifizierung werden Access- und Refresh-Tokens verwendet, die über Cookies zwischen Frontend und Backend übertragen werden.

Verwendete JWT-Komponenten:

```text
Access Token
Refresh Token
```

## Token-Erstellung

Bei der Anmeldung eines Benutzers werden ein Access Token und ein Refresh Token erstellt. Diese werden in Cookies gespeichert und für die Authentifizierung bzw. Erneuerung der Authentifizierung verwendet.

## Authentifizierte Anfragen

Geschützte API-Anfragen werden mithilfe des Access Tokens authentifiziert. Das Token wird über das Cookie an das Backend übermittelt und vom Backend auf seine Gültigkeit überprüft.

Ist das Access Token abgelaufen, kann mithilfe des Refresh Tokens ein neues Access Token angefordert werden.

Die Authentifizierung erfolgt somit nicht über einen Authorization-Header, sondern über die zwischen Frontend und Backend übertragenen Cookies.

---

# API Endpunkte

Die Anwendung stellt folgende API-Endpunkte bereit:

| Nr. | Methode  | Endpunkt               | Name            | Beschreibung                                                         |
| --- | -------- | ---------------------- | --------------- | -------------------------------------------------------------------- |
| 1   | POST     | `api/register/`        | registration    | User registrieren                                                    |
| 2   | POST     | `api/login/`           | login           | User einloggen                                                       |
| 3   | POST     | `api/logout/`          | logout          | User ausloggen                                                       |
| 4   | POST     | `api/token/refresh/`   | token_refresh   | mit Hilfe des Refresh-Tokens einen neuen Zugriffstoken angefordert   |
| 5   | POST     | `api/quizzes/`         | quiz-list       | Erstellt ein neues Quiz mit dessen Fragen                            |
| 6   | GET      | `api/quizzes/`         | quiz-list       | Ruft alle Quizzes mit deren Fragen                                   |
| 7   | GET      | `api/quizzes/<pk>/`    | quiz-detail     | Gibt ein einzelnen Quiz mit dessen Fragen zurück                     | 
| 8   | PATCH    | `api/quizzes/<pk>/`    | quiz-detail     | Aktualisiert einen bestehenden Quiz                                  |
| 9   | DELETE   | `api/quizzes/<pk>/`    | quiz-detail     | Löscht ein Quiz mit deren fragen                                     |

---

# Projektstruktur

```text
Quizly
│
├── .gitignore
├── db.sqlite3
├── .env
├── manage.py
├── requirements.txt
├── README.MD
├── README_DE.MD
|
├── media/tmpl_audios/
|
├── services
|    └── transcriber.py
|
├── templates
|    └── prompt_template.py
│
├── tests
|    └── helpers.py
|
├── tools
|    └── ffmpeg.exe
|
├── core
│   ├── settings.py
|   ├── authentication.py
|   ├── test_runner.py
│   └── urls.py
│
├── auth_app
│   ├── models.py
|   ├── admin.py
│   ├── migrations/
│   ├── tests
|   |   ├── test_login.py
|   |   ├── test_logout.py
|   |   ├── test_registration.py
|   |   └── test_token_refresh.py
|   |
|   └── api
|       ├── serializers.py
|       ├── urls.py
|       └── views.py
│
└── quiz_management_app
    ├── models.py
    ├── admin.py
    ├── migrations/
    ├── api
    |   ├── permissions.py
    |   ├── serializers.py
    |   ├── urls.py
    |   └── views.py
    |
    └── tests
        ├── tests.py
        └── data.py
```

---

# Tests

Das Projekt enthält automatisierte Tests.

Alle Tests ausführen:

```bash
python manage.py test
```

Nur die Tests einer bestimmten Testdatei ausführen:

```bash
python manage.py test auth_app.tests.test_login
```

```bash
python manage.py test auth_app.tests.test_logout
```

```bash
python manage.py test auth_app.tests.test_registration
```

```bash
python manage.py test auth_app.tests.test_token_refresh
```

```bash
python manage.py test quiz_management_app.tests.tests
```

---

# Technische Besonderheiten

* Kommunikation zwischen Frontend und Backend über eine REST API
* JWT-Authentifizierung über HTTP-Cookies
* Verwendung von Access- und Refresh-Tokens zur Verwaltung der Authentifizierung
* Lokale Transkription von Audiodateien mit OpenAI Whisper
* Automatische Audioverarbeitung mit FFmpeg
* Verarbeitung der transkribierten Texte durch strukturierte Prompts
* Verarbeitung und Aufbereitung der KI-generierten Antworten im Backend

---

# Lizenz

© 2026 Leonard Fritzmann

Alle Rechte vorbehalten.

Dieses Projekt dient ausschließlich Lern- und Portfoliozwecken. Eine Nutzung, Vervielfältigung oder Weitergabe des Quellcodes ist ohne ausdrückliche Genehmigung nicht gestattet.

---

# Kontakt

Bei Fragen oder Anmerkungen:

* E-Mail: contact@leonard-fritzmann.de