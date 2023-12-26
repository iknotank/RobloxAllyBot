import requests
from random import randint
import time
import threading
import os
import traceback
from dotenv import load_dotenv
from colorama import Fore, init, Style
from collections import deque

init()

GREEN = Fore.GREEN
RESET = Style.RESET_ALL

load_dotenv()

group = os.getenv('GROUP')
allies = os.getenv('TYPE')
delay = int(os.getenv('DELAY', default=1))
threads = int(os.getenv('THREADS', default=1))
type = os.getenv('TYPE')
min_random_id = int(os.getenv('MIN_RANDOM_ID', default=0))
max_random_id = int(os.getenv('MAX_RANDOM_ID', default=33176270))

def load_cookies():
    try:
        with open('cookies.txt', 'r') as file:
            cookies = file.read().splitlines()
            if not cookies:
                print("Error: cookie file is empty")
                time.sleep(2)
                exit()
            return deque(cookies)  # Use deque to manage rotation
    except Exception as e:
        print(f'Error in loading cookies: {e}')
        traceback.print_exc()
        return None

def send_ally_request():
    cookies_queue = load_cookies()
    if not cookies_queue:
        print("Cookie failure")
        return

    while True:
        try:
            random_id = randint(min_random_id, max_random_id)
            cookies = {'.ROBLOSECURITY': cookies_queue[0]}  # Get the first cookie in the queue

            login_response = requests.post('https://auth.roblox.com/v1/login', cookies=cookies)
            token = login_response.headers.get('x-csrf-token')

            headers = {'x-csrf-token': token}

            send_ally = requests.post(
                f'https://groups.roblox.com/v1/groups/{group}/relationships/{allies}/{random_id}',
                headers=headers,
                cookies=cookies
            )

            if send_ally.status_code == 200:
                print(GREEN + f'Ally sent to {random_id} ⚉ ' + RESET)
            elif send_ally.status_code == 429:
                print(GREEN + 'Rate limited 400s....⚇' + RESET)
                time.sleep(400)
            else:
                print(GREEN + f'Failed to send {allies} request to {random_id}' + RESET)

            # Rotate cookies queue
            cookies_queue.rotate(-1)
        except Exception as e:
            print(GREEN + f'Error: {e}' + RESET)
            traceback.print_exc()
        time.sleep(delay)

def main():
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
       Made by a14rl      |  $$$$$$/                                    
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

    for _ in range(threads):
        t = threading.Thread(target=send_ally_request)
        t.start()

if __name__ == "__main__":
    main()
