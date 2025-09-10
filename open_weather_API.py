import requests, os, sys, argparse
import requests.cookies
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
api = os.getenv("api_key")

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--city")
    return parser

try:
    if __name__ == "__main__":
        parse = create_parser()
        namespace = parse.parse_args(sys.argv[1:])
        print(f"City: {namespace.city}")
        url_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={namespace.city}&limit=1&appid={api}"
        result = []
        response_geo = requests.get(url=url_geo)
        response_geo.raise_for_status()
        lat, lon = response_geo.json()[0]["lat"], response_geo.json()[0]["lon"]
        url_weather = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=daily,hourly,minutely&appid={api}"
        response_weather = requests.get(url=url_weather, params={"units": "metric", "lang": "ru"})
        current = response_weather.json()["current"]

        for i, key in enumerate(current):
            if key == "dt":
                result.append(f"date time: {datetime.fromtimestamp(current.get(key))}")
                continue
            if i < 3:
                result.append(f"{key}: {datetime.fromtimestamp(current.get(key))}")
                continue
            if key == "weather":
                result.append(f"Описание: {current["weather"][0]["description"]}")
                continue
            result.append(f"{key}: {current.get(key)}")

        print("\n".join(result))
except requests.exceptions.RequestException as err:
    print(f"Response error {err}")