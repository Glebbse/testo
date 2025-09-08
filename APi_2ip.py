import requests


url = "https://api.2ip.io?token=atft3yxzmxe4fruv"

try:
    response = requests.get(url=url)
    response.raise_for_status()
    ip = response.json()["ip"]
    print(ip)
except requests.exceptions.RequestException as err:
    print(f"Response error {err}")
except KeyError as er:
    print(f"Error key {er}")
