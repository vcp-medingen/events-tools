import os
import pymysql
from datetime import date

from dotenv import load_dotenv
def init():
    load_dotenv()
    global db
    global cursor
    db = pymysql.connect(host=os.environ.get("MYSQL_HOST"), user=os.environ.get("MYSQL_USER"), password=os.environ.get("MYSQL_PASSWORD"), database=os.environ.get("MYSQL_DATABASE"))
    cursor = db.cursor()

def execute(sql):
    cursor.execute(sql)
    return cursor.fetchall()

def get_events():
    return execute("SELECT * FROM wp_em_events")

def get_events(rsvp_end_date: date):
    return execute(f"SELECT event_id, event_name FROM wp_em_events WHERE event_rsvp_date = '{rsvp_end_date}'")

def get_bookings(event_id: int):
    return execute(f"SELECT booking_meta FROM wp_em_bookings WHERE event_id = {event_id}")

def close():
    db.close()