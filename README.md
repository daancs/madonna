# Agile Software Project Management - Madonna
Trello for Sprint backlogs: https://trello.com/b/AwWUfX1h/scrum-board

# Project Structure
```
madonna
│     
│
└───**docs**
│   │
│   └───IndividualReflections
|   |
│   └───misc (has info on how to run)
|   |
│   └───Project scope (mockup, description etc)
|   |
│   └───Team-reflections
│   
│   
└───**flask**
|   |
│   └───db (sql file)
|   |
│   └───export (where an export of a table goes)
|   |
│   └───flaskr (basically the source-folder, all code for application is here)
|   |
│   └───venv (the virtual environment for the application, this has to be activated to run if not using docker)
```

# How to run

## Med Docker
- Installera Docker
- Öppna kommandotolken (eller godtycklig command-line där docker kan köras (prova att skriva `docker` för att kolla))
- Navigera in i madonna mappen genom `cd` där `docker-compose.yml` filen är.
- Kör `docker-compose up` i kommandotolken. 
- Gå till `localhost:5000` i din webbläsare.

## Utan Docker

1. Installera python

2. Öppna en terminal och navigera till mappen `flask`

3. Skapa ett "virtual environment" (om du inte har mappen venv)

    Windows: `py -3 -m venv venv`

    Linux/macOS: `python3 -m venv venv`

4. Aktivera ditt environment (detta behöver göras varje gång man öppnar en ny terminal, se nedan).

    Windows: `venv\Scripts\activate`

    Linux/macOS: `source venv/bin/activate`

    Ditt environment är aktiverat om du ser `(venv)` längst ner till vänster i terminalen.

5. Installera flask och andra libraries

    `pip install flask psycopg2`
    `pip install deepdiff`

### Starta webbservern

1. Öppna en terminal och navigera till mappen `flask`

2. Aktivera ditt environment ifall det inte är det.

    Windows: `venv\Scripts\activate`

    Linux/macOS: `source venv/bin/activate`

3. Kör följande kommandon för att "berätta" vart flask ska köras och sätta lösenordet för databasen

    Linux/macOS:
    ```
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    export DB_PASSWORD=*Ditt Lösenord*
    ```

    Windows PowerShell:
    ```
    $env:FLASK_APP = "flaskr"
    $env:FLASK_ENV = "development"
    $env:DB_PASSWORD = *Ditt Lösenord*
    ```

    Windows CMD:
    ```
    set FLASK_APP = "flaskr"
    set FLASK_ENV = "development"
    set DB_PASSWORD = *Ditt Lösenord*
    ```
4. Starta flask genom att köra `flask run` i terminalen

5. För att se sidan, öppna http://localhost:5000 i en webbläsare
