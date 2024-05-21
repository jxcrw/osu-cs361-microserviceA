#!/usr/bin/env python3
"""Send a request to tinyweather."""

import zmq


# Config.
PORT_NUMBER = 5555
city = "Las Vegas"

# Create socket.
print("Connecting to server...")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(f'tcp://localhost:{PORT_NUMBER}')

# Send request and wait for response.
print(f"Sending request: {city}")
socket.send_string(city)

# Get response.
response = socket.recv_json()
print(f"Received response: {response}\n")
