import telegramfunctions as t
import time
from datetime import datetime
import answerfinder as a
import sensibledata as s
import os

os.environ['TZ'] = 'Europe/Rome'
time.tzset()

def log(message):
    logfile = open("chatlog.txt", "a")
    logfile.write(message+"\n")
    print(message)
    logfile.close()

def getName(id):
    return s.knownIds.get(str(id),"")

last_update_id = None

t.send_message("BOT BOOTED", s.MYID)

while True:
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    updates = t.get_updates(last_update_id)
    if "result" in updates and len(updates["result"]) > 0:
        last_update_id = t.get_last_update_id(updates) + 1
        text, id, person_id = t.get_last_chat_id_and_text(updates)
        answer = a.find_answer(text)
        t.send_message(answer, id)
        log(date_time + "\n" + str(person_id) + ":" + getName(person_id) + ": \"" + text +"\" " + ".\nBOT REPLIED: \"" + answer + "\" \n")
    time.sleep(0.5)

