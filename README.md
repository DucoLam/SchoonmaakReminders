# 📲 WhatsApp HGS Reminder Bot

Deze tool stuurt automatisch WhatsApp-berichten naar huisgenoten over
hun taken, gebaseerd op een Google Sheets rooster.

## 🚀 Features

-   Leest telefoonnummers uit Google Sheets\
-   Leest rooster uit Google Sheets\
-   Stuurt gepersonaliseerde WhatsApp-berichten\
-   Ondersteunt automatische dagelijkse uitvoering\
-   Gaat veilig om met lege velden (NaN)

------------------------------------------------------------------------

## 📊 Verwachte Google Sheets structuur

### Nummers

  Naam   Nummer
  ------ -------------
  Taco   31657708366

------------------------------------------------------------------------

### Rooster

  ------------------------------------------------------------------------------
  Datum       WC        Douche   Keuken 1  Keuken 2  GR1     GR2       Huisman
  ----------- --------- -------- --------- --------- ------- --------- ---------
  23-3-2026   Michiel            Pino      Sjoerd    Nelis   Marleen   Remco

  ------------------------------------------------------------------------------

⚠️ Datumformaat: **DD-MM-YYYY**

------------------------------------------------------------------------

## ⚙️ Installatie

### 1. Dependencies installeren

``` bash
pip install pandas pywhatkit schedule python-dotenv
```

------------------------------------------------------------------------

### 2. Maak een `.env` bestand

``` env
NUMMERS_ID=your_google_sheet_id
ROOSTER_ID=your_google_sheet_id
```

De ID is het stuk uit de URL:

    https://docs.google.com/spreadsheets/d/DIT_STUK/export?format=csv

------------------------------------------------------------------------

## ▶️ Gebruik

### Testmodus

``` bash
python main.py
```

Gebruikt een vaste testdatum.

------------------------------------------------------------------------

### Productiemodus

Pas aan:

``` python
main(for_real=True)
```

Start daarna:

``` bash
python main.py
```

Dit: - draait elke dag om **09:00** - stuurt berichten voor **morgen**

------------------------------------------------------------------------

## 🧠 Werking

1.  Haalt nummers op → `{naam: nummer}`\
2.  Haalt rooster op → DataFrame\
3.  Selecteert morgen\
4.  Stuurt berichten per taak

------------------------------------------------------------------------

## ⚠️ Belangrijk

### WhatsApp Web

-   Eerste keer: QR-code scannen\
-   Browser moet open blijven

------------------------------------------------------------------------

### Timing

-   `wait_time` bepaalt wachttijd\
-   Te laag → berichten worden niet verstuurd

------------------------------------------------------------------------

### Spam

-   Te veel berichten = kans op blokkade

------------------------------------------------------------------------

## 🐛 Problemen

### Chat opent maar verstuurt niet

-   Verhoog `wait_time`
-   Zorg dat WhatsApp Web volledig geladen is
