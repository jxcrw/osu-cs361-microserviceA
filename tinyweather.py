#!/usr/bin/env python3
"""Receive a request and send back a response."""

import json
import requests
import zmq


# Config
API_KEY = 'e72c934f51629bffbdf40b18ad0151bb'
RAIN_CATEGORIES = ['Thunderstorm', 'Drizzle', 'Rain']


# Create socket.
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


# Process requests.
print('Waiting for requests...')
while True:
    # Get request from client.
    city = socket.recv_string()
    print(f"Received request: {city}")

    # Get weather from OpenWeatherMap.
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()

        # Parse weather data.
        weather = data['weather'][0]['main']
        time_current = data['dt']
        time_sunrise = data['sys']['sunrise']
        time_sunset = data['sys']['sunset']

        # Summarize weather data.
        is_raining = weather in RAIN_CATEGORIES
        is_day = time_sunrise <= time_current <= time_sunset
        weather_summary = {'city': city, 'is_day': is_day, 'is_raining': is_raining}
        weather_summary_json = json.dumps(weather_summary)
    else:
        print("Error in OpenWeatherMap HTTP request.")

    # Send response back to client.
    socket.send_json(weather_summary_json)

