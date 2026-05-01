import pandas as pd
import pywhatkit
import time
import schedule
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

def send(phone, message, time):
    """
    Sends a WhatsApp message to the given phone number with the given message after waiting for the given time.
    phone: str, in format +31612345678
    message: str, the message to send
    time: int, the time to wait before sending the message, in seconds
    """
    pywhatkit.sendwhatmsg_instantly(
        phone_no=phone,
        message=message,
        wait_time=time,
        tab_close=True,
    )

def fetch_nummers():
    """
    Fetches the phone numbers from the Google Sheets document and returns a dictionary with the names as keys and the numbers as values.
    """
    nummers_id = os.getenv("NUMMERS_ID")
    url = f"https://docs.google.com/spreadsheets/d/{nummers_id}/export?format=csv"
    nummers_df = pd.read_csv(url)
    ## Format:
    # Naam | Nummer
    #0 Taco | 31657708366
    nummers_df = dict(zip(nummers_df["Naam"], nummers_df["Nummer"]))
    print(nummers_df)
    return nummers_df

def fetch_rooster(datum): 
    """
    Fetches the schedule from the Google Sheets document and returns a DataFrame with the schedule for the given date.
    datum: datetime, the date for which to fetch the schedule
    """
    rooster_id = os.getenv("ROOSTER_ID")
    url = f"https://docs.google.com/spreadsheets/d/{rooster_id}/export?format=csv"
    rooster_df = pd.read_csv(url)

    ## Format:
    # Datum | Naam
    #0 2024-06-01 | Taco
    rooster_df["Datum"] = pd.to_datetime(rooster_df["Datum"])    
    rooster_df.set_index("Datum", inplace=True)
    print(rooster_df.loc[datum])
    return rooster_df

def remind_hgs(datum, rooster_df, time=15):
    """
    Reminds the housemates of their tasks for the next day by sending them a WhatsApp message.
    datum: datetime, the date for which to remind the housemates
    rooster_df: DataFrame, the schedule for the given date
    time: int, the time to wait before sending the message, in seconds
    """
    nummers = fetch_nummers()
    # WC Taak
    wc_persoon = rooster_df.loc[datum]["WC"]
    if pd.isna(wc_persoon):
        print("WC Taak: niemand ingepland")
    else:
        message = f"Hallo {wc_persoon}, je hebt wc taak morgen!"
        send(f"+{nummers[wc_persoon]}", message, time)

    # Douche Taak
    douche_persoon = rooster_df.loc[datum]["Douche"]
    if pd.isna(douche_persoon):
        print("Douche Taak: niemand ingepland")
    else:
        message = f"Hallo {douche_persoon}, je hebt douche taak morgen!"
        send(f"+{nummers[douche_persoon]}", message, time)

    # Keuken Taak
    keuken_persoon_1 = rooster_df.loc[datum]["Keuken 1"]    
    keuken_persoon_2 = rooster_df.loc[datum]["Keuken 2"]
    if pd.isna(keuken_persoon_1) or pd.isna(keuken_persoon_2):
        print("Keuken Taak: een of beide personen niet ingepland")
    else:
        message_one = f"Hallo {keuken_persoon_1}, je hebt keukentaak met {keuken_persoon_2} morgen!" 
        send(f"+{nummers[keuken_persoon_1]}", message_one, time)

        message_two = f"Hallo {keuken_persoon_2}, je hebt keukentaak met {keuken_persoon_1} morgen!"
        send(f"+{nummers[keuken_persoon_2]}", message_two, time)

    # GR Taak
    gr_persoon_1 = rooster_df.loc[datum]["GR1"]
    gr_persoon_2 = rooster_df.loc[datum]["GR2"]
    if pd.isna(gr_persoon_1) or pd.isna(gr_persoon_2):
        print("GR Taak: een of beide personen niet ingepland")
    else:
        message_one = f"Hallo {gr_persoon_1}, je hebt GR taak met {gr_persoon_2} morgen!"
        send(f"+{nummers[gr_persoon_1]}", message_one, time)

        message_two = f"Hallo {gr_persoon_2}, je hebt GR taak met {gr_persoon_1} morgen!"
        send(f"+{nummers[gr_persoon_2]}", message_two, time)

    # Huisman Taak
    huisman_persoon = rooster_df.loc[datum]["Huisman"]
    if pd.isna(huisman_persoon):
        print("Huisman Taak: niemand ingepland")
    else:
        message = f"Hallo {huisman_persoon}, je hebt huischman taak deze week!"
        send(f"+{nummers[huisman_persoon]}", message, time)

def job(time=15):
    """"
    Job to run every day at 09:00, which fetches the schedule for the next day and reminds the housemates of their tasks.
    time: int, the time to wait before sending the message, in seconds
    """
    dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dt = dt + timedelta(days=1)
    rooster_df = fetch_rooster(dt)
    remind_hgs(dt, rooster_df, time=time)


def main(for_real=False, time=15):
    if for_real:
        schedule.every().day.at("09:00").do(job, time=time)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        dt = datetime(2026, 3, 26) # Change this to the date of today + one day
        rooster_df = fetch_rooster(dt)
        remind_hgs(dt, rooster_df, time=time)
        if os.path.exists("PyWhatKit_DB.txt"):
            os.remove("PyWhatKit_DB.txt")


if __name__ == "__main__":
    main(for_real=True, time=20)


