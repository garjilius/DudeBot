from threading import Timer
import telegramfunctions as t
import time
from datetime import datetime
import answerfinder as a
import sensibledata as s
import os
import traceback

active = True

os.environ['TZ'] = 'Europe/Rome'
time.tzset()

def toggleBot():
    global active
    active^=True

def manageBot(input,chatid):
    a = 0
    global active
    if not active:
        active = True
        t.send_message("BOT IS BACK BITCHES", chatid)
        return
    for word in input.split():
        try:
            a = (float(word))
        except ValueError:
            pass
    active = False
    timersleep = Timer(a*60, toggleBot)
    t.send_message("SLEEPING FOR " + str(a) + "m", chatid)
    timersleep.start()

def log(message):
    logfile = open("chatlog.txt", "a")
    logfile.write(message + "\n")
    print(message)
    logfile.close()


def getName(id):
    return s.knownIds.get(str(id), "")

def sleepFor(timeToSleep):
    time.sleep(timeToSleep * 60)

last_update_id = None

t.send_message("BOT BOOTED", s.MYID)

while True:
    try:
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        updates = t.get_updates(last_update_id)
        if "result" in updates and len(updates["result"]) > 0:
            last_update_id = t.get_last_update_id(updates) + 1
            text, id, person_id = t.get_last_chat_id_and_text(updates)
            if len(text) > 0:
                if(a.found(text,"BOT SLEEP")):
                    manageBot(text,id)
                if(a.found(text,"BOT RESUME NOW")):
                    manageBot(text,id)
                if active:
                    answer = a.find_answer(text, id)
                    # t.send_message(answer, id)
                    # log("\n"+date_time + "\n" + str(person_id) + "(" + getName(person_id) + "): \"" + text +"\" ")
                    if len(answer) > 0:
                        log("BOT REPLIED: \"" + answer + "\"")
    except:
        traceback.print_exc()
    time.sleep(0.5)


