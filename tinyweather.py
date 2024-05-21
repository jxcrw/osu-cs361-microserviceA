#!/usr/bin/env python3
"""Receive a request and send back a response."""

import json
import requests
import zmq


# ┌─────────────────────────────────────────────────────────────────────────────
# │ CONFIG
# └─────────────────────────────────────────────────────────────────────────────
PORT_NUMBER = 5555
OPENWEATHERMAP_API_KEY = 'e72c934f51629bffbdf40b18ad0151bb'
RAIN_CATEGORIES = ['Thunderstorm', 'Drizzle', 'Rain']


# ┌─────────────────────────────────────────────────────────────────────────────
# │ Functions
# └─────────────────────────────────────────────────────────────────────────────
def open_socket(port_number: int):
    """Open a socket for communication on the specified port number."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f'tcp://*:{port_number}')
    return socket


def summarize_weather(city: str) -> str:
    """Create a tiny JSON summary of the current weather in the specified city."""
    # Get weather data from OpenWeatherMap API.
    weather_summary = dict()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        # Parse weather data.
        data = response.json()
        weather = data['weather'][0]['main']
        time_current = data['dt']
        time_sunrise = data['sys']['sunrise']
        time_sunset = data['sys']['sunset']

        # Summarize weather data.
        is_raining = weather in RAIN_CATEGORIES
        is_day = time_sunrise <= time_current <= time_sunset
        weather_summary = {'city': city, 'is_day': is_day, 'is_raining': is_raining}
    else:
        print("Error in OpenWeatherMap HTTP request.")

    weather_summary_json = json.dumps(weather_summary)
    return weather_summary_json


def process_requests(socket) -> None:
    """Process requests to the tinyweather microservice."""
    print('Waiting for requests...')
    while True:
        # Get request from client.
        city = socket.recv_string()
        print(f"Received request: {city}")

        # Build weather summary.
        weather_summary_json = summarize_weather(city)

        # Send weather summary back to client.
        socket.send_json(weather_summary_json)


if __name__ == '__main__':
    socket = open_socket(PORT_NUMBER)
    process_requests(socket)
