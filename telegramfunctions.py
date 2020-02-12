import requests
import json
import urllib.parse
import sensibledata as d

TOKEN = d.TOKEN
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#TELEGRAM BOT FUNCTIONS
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    #print (url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    try:
        num_updates = len(updates["result"])
    except:
        num_updates = 1
    last_update = num_updates - 1
    try:
        text = updates["result"][last_update]["message"]["text"]
    except:
        text = ""
    #print(updates)
    try:
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    except:
        chat_id = ""
    try:
        person_id = updates["result"][last_update]["message"]["from"]["id"]
    except:
        person_id = ""
    return (text, chat_id, person_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)



