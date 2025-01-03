from datetime import timedelta, date

from phpserialize import loads

import email_helper
import sql_helper

sql_helper.init()
email_helper.init()

yesterday = date.today() - timedelta(days=1)

events = sql_helper.get_events(yesterday)

for event in events:
    print(f"Found event with ID {event[0]} and name {event[1]}. ")
    bookings = sql_helper.get_bookings(event[0])
    if len(bookings) == 0:
        print("No bookings found for this event.")
        continue
    gdpr_allowed = []
    gdpr_forbidden = []
    for bookings in bookings:
        booking_meta = loads(bytes(bookings[0], 'utf-8'), decode_strings=True)
        name = booking_meta["registration"]["name"]
        email = booking_meta["registration"]["user_email"]
        if booking_meta["booking"]["fotoerlaubnis"] == "1":
            gdpr_allowed.append({
                "name": name,
                "email": email,
                "legal_guardian": booking_meta["booking"]["unterschrift_eines_erziehungsberechtigten"]
            })
        else:
            gdpr_forbidden.append({
                "name": name,
                "email": email,
            })
    print("GDPR allowed:" + str(gdpr_allowed))
    print("GDPR forbidden:" + str(gdpr_forbidden))
    list_gdpr_allowance = ""
    for participant in gdpr_allowed:
        list_gdpr_allowance += f"Name: {participant['name']}\nEmail: {participant['email']}\nErlaubt durch Erziehungsberechtigten: {participant['legal_guardian']}\n\n"

    list_gdpr_forbidden = ""
    if len(gdpr_forbidden) == 0:
        list_gdpr_forbidden = "Keine Teilnehmer haben die Fotoerlaubnis verweigert."
    for participant in gdpr_forbidden:
        list_gdpr_forbidden += f"Name: {participant['name']}\nEmail: {participant['email']}\n\n"
    message = f"""
Moin Redaktion,
die Anmeldefrist für die Veranstaltung {event[1]} ist abgelaufen. Folgend sind die Fotoerlaubnisse der Teilnehmer:
Erlaubt:

{list_gdpr_allowance}

Nicht erlaubt:
{list_gdpr_forbidden}

Gut Pfad
IT-Beauftragter
    """

    email_helper.send_mail("redaktion@vcp-medingen.de", f"Fotoerlaubnisse für {event[1]}", message)

sql_helper.close()
email_helper.close()