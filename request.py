#!/usr/bin/env python3
"""Send a request to tinyweather."""

import zmq


# Configure city.
city = "Las Vegas"

# Create socket.
print("Connecting to server...")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Send request and wait for response.
print(f"Sending request: {city}")
socket.send_string(city)

# Get response.
response = socket.recv_json()
print(f"Received response: {response}\n")
