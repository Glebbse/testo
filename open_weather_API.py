import requests, os, sys, argparse
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
api = os.getenv("api_key")
if not api:
    sys.exit("API_KEY hasn't been found. Check .env file")

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--city", required=True, help='City name. Example: London')
    return parser

result = []
if __name__ == "__main__":
    parse = create_parser()
    namespace = parse.parse_args(sys.argv[1:])
    url_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={namespace.city}&limit=1&appid={api}"
    try:
        response_geo = requests.get(url=url_geo)
        response_geo.raise_for_status()

    except requests.exceptions.RequestException as err:
        print(f"Response error {err}")
    except KeyError as er:
        print(f"Key error {er}")
    geo_data = response_geo.json()
    if not geo_data:
        sys.exit(f"City {namespace.city} hasn't been found.")

    lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
    url_weather = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=daily,hourly,minutely&appid={api}"
    try:
        response_weather = requests.get(url=url_weather, params={"units": "metric", "lang": "ru"})
        response_weather.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Response error {err}")
    except KeyError as er:
        print(f"Key error {er}")
    print(f"City: {namespace.city}\ntimezone: {response_weather.json()['timezone']}")
    current = response_weather.json()['current']

    for i, key in enumerate(current):
        if key == "dt":
            result.append(f"date time: {datetime.fromtimestamp(current.get(key))}")
            continue
        if key in ("sunrise", "sunset"):
            result.append(f"{key}: {datetime.fromtimestamp(current.get(key))}")
            continue
        if key == "weather":
            result.append(f"Описание: {current['weather'][0]['description']}")
            continue
        result.append(f"{key}: {current.get(key)}")

    print("\n".join(result))
