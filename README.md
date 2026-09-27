# Movie Recommendation App

Eine Flask-Web-App, die zu einem Film ähnliche Filme vorschlägt.
Die Filmdaten (TMDB) liegen als RDF in einem **Apache Jena Fuseki**-Server
und werden per SPARQL abgefragt. Die Ähnlichkeit wird mit TF-IDF über
Beschreibung und Genres berechnet.

## Voraussetzungen

- Python 3
- Java 21 oder neuer (für Fuseki)
- [Apache Jena Fuseki](https://jena.apache.org/download/)
- Die Datei `tmdb.ttl` mit den Filmdaten (nicht im Repo, weil zu groß)

Empfohlene Ordnerstruktur:

```
film-reccomandation/
├── apache-jena-fuseki-6.1.0/   ← Fuseki
├── tmdb.ttl                    ← Filmdaten
└── Film_recommandation/        ← dieses Repo
```

## Einmalige Einrichtung

**1. Python-Pakete installieren** (im Ordner `Film_recommandation`):

```powershell
python -m pip install -r requirements.txt
```

**2. Daten in Fuseki laden:**

1. Fuseki starten (im Fuseki-Ordner): `.\fuseki-server.bat`
2. http://localhost:3030 öffnen
3. Ein Dataset mit dem Namen **`TMDB`** anlegen (Typ „Persistent (TDB2)“,
   dann bleiben die Daten auch nach einem Neustart erhalten)
4. Beim Dataset `TMDB` auf „add data“ gehen und `tmdb.ttl` hochladen

## App starten

Du brauchst zwei PowerShell-Fenster.

**Fenster 1 – Fuseki:**

```powershell
cd apache-jena-fuseki-6.1.0
.\fuseki-server.bat
```

**Fenster 2 – App:**

```powershell
cd Film_recommandation
python app.py
```

Dann http://127.0.0.1:5000 im Browser öffnen.

## Häufige Probleme

| Meldung | Lösung |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Pakete installieren: `python -m pip install -r requirements.txt` |
| „Could not connect to the movie database“ | Fuseki läuft nicht → Fenster 1 starten |
| „Fuseki is running, but the dataset TMDB was not found“ | Dataset `TMDB` in Fuseki anlegen (siehe Einrichtung) |
| „The dataset TMDB contains no movies“ | `tmdb.ttl` in Fuseki hochladen |
| Fuseki: `Data service name already registered: /TMDB` | Das Dataset existiert schon → Fuseki ohne `--file` starten: `.\fuseki-server.bat` |
| `Activate.ps1 ... Ausführung von Skripts ist deaktiviert` | Nur bei venv: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

## Projektstruktur

| Datei | Inhalt |
|---|---|
| `app.py` | Flask-App: lädt die Filme einmal, verarbeitet die Suche |
| `sparql_queries.py` | SPARQL-Abfrage, die alle Filme aus Fuseki holt |
| `movie_search.py` | Titelsuche: exakt, Teiltreffer, Tippfehler |
| `recommender.py` | TF-IDF und Ähnlichkeitsberechnung |
| `templates/index.html` | Die Webseite |
| `static/style.css` | Eigenes CSS (zusätzlich zu Bootstrap) |
