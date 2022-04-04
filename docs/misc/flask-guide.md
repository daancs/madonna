## Lite basic terminal syntax
`ls` lista alla mappar i den nuvarande mappen (Linux,mac,powershell)

`dir` lista alla mappar i den nuvarande mappen (CMD)

`cd folder` navigera till mappen folder, byt ut vid behov

`cd ..` gå upp en mapp.

## Installera Flask
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

## Starta webbservern

1. Öppna en terminal och navigera till mappen `flask`

2. Aktivera ditt environment ifall det inte är det.

    Windows: `venv\Scripts\activate`

    Linux/macOS: `source venv/bin/activate`

3. Kör följande kommandon för att "berätta" vart flask ska köras

    Linux/macOS:
    ```
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    ```

    Windows PowerShell:
    ```
    $env:FLASK_APP = "flaskr"
    $env:FLASK_ENV = "development"
    ```

    Windows CMD:
    ```
    set FLASK_APP = "flaskr"
    set FLASK_ENV = "development"
    ```
4. Starta flask genom att köra `flask run` i terminalen

5. För att se sidan, öppna http://localhost:5000 i en webbläsare
