import requests
import os
from dotenv import load_dotenv

def get_tg_private_information():
    load_dotenv()
    return os.getenv("BOT_KEY"), os.getenv("CHAT_ID")

def send_to_tg(post_title, post_link):

    bot_key, chat_id = get_tg_private_information()
    s = "-----------------------------------------------" + "\n"
    s += "\n"
    s += "New governance forum posted or comment" + "\n"
    s += "\n"
    s += "Forum title: " + post_title + "\n"
    s += "Post link: " + post_link


    tg_url = "https://api.telegram.org/{}/sendMessage".format(bot_key)

    requests.post(tg_url, json={'chat_id': chat_id, 'text': s})

