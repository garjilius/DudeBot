import telegramfunctions as t
import time
import datetime
import answerfinder as a
import sensibledata as s

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
    updates = t.get_updates(last_update_id)
    if "result" in updates and len(updates["result"]) > 0:
        last_update_id = t.get_last_update_id(updates) + 1
        text, id, person_id = t.get_last_chat_id_and_text(updates)
        t.send_message(a.find_answer(text), id)
        log(text +"\" by " + str(person_id) + ":" + getName(person_id) + " at " + str(datetime.datetime.now().time()))
    time.sleep(0.5)

