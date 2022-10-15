#!/usr/bin/env python

import json
import platform

CONFIG_FILE_NAME = "config.json"

def is_raspberry_pi() -> bool:
  return platform.machine() in ('armv7l', 'armv6l')

if is_raspberry_pi():
  import RPi.GPIO as GPIO
  from mfrc522 import SimpleMFRC522
  import vlc
  reader = SimpleMFRC522()

config_object = None

# Fetch the configs from a file
with open(CONFIG_FILE_NAME, 'r') as openfile:
  # Reading from json file
  config_object = json.load(openfile)

try:
  while True:
    try:
      print("Waiting to read a card...")

      # TODO: Add a line for reading the RFID card
      if is_raspberry_pi():
        id, text = reader.read()
      else:
        id = "1234"

      print("A card found: " + id)

      if id not in config_object:
        # Make a beep
        print('\a \a \a')
        print("This card is not configured.")
      else:
        card_config = config_object[id]
        print(card_config["description"])
        # TODO: handle the card properly depending on its configuration (switch language, play media, stop, shutdown...)
        if player != None: player.stop()
        player = vlc.MediaPlayer(card_config["media"])
        player.play()
    except ValueError:
      print("Sorry, I didn't understand that.")
      # Better try again... Return to the start of the loop
      continue
finally:
  if is_raspberry_pi():
    GPIO.cleanup()