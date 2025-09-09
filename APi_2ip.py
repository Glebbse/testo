import os
import requests

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


TOKEN = os.getenv("TOKEN")
url = f"https://api.2ip.io?token={TOKEN}"

try:
    response = requests.get(url=url)
    response.raise_for_status()
    ip = response.json()["ip"]
    print(ip, response.json())
except requests.exceptions.RequestException as err:
    print(f"Response error {err}")
except KeyError as er:
    print(f"Error key {er}")
