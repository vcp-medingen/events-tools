import os
import pymysql

from dotenv import load_dotenv
def init():
    load_dotenv()
    global db
    global cursor
    db = pymysql.connect(host=os.environ.get("MYSQL_HOST"), user=os.environ.get("MYSQL_USER"), password=os.environ.get("MYSQL_PASSWORD"))
    cursor = db.cursor()

def execute(sql):
    return cursor.execute(sql)