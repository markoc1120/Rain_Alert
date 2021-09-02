import requests
import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH = os.environ.get('TWILIO_AUTH')
OW_ENDPOINT = 'https://api.openweathermap.org/data/2.5/onecall'
OW_API_KEY = os.environ.get('API_KEY')
parameters = {
    'lat': 42.36,
    'lon': -71.05,
    'exclude': 'current,minutely,daily',
    'appid': OW_API_KEY,
}

response = requests.get(url=OW_ENDPOINT, params=parameters)
response.raise_for_status()

data = response.json()['hourly']
weather_description = [0 for item in data[:12] if item['weather'][0]['id'] < 700]

if 0 in weather_description:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH)
    message = client.messages \
        .create(body="It's going to rain, remember to bring an umbrella.",
                from_=os.environ.get('FROM_PHONE'),
                to=os.environ.get('MY_PHONE')
                )

    print(message.status)
