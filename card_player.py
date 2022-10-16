#!/usr/bin/env python

import json
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import vlc

reader = SimpleMFRC522()
CONFIG_FILE_NAME = "config.json"
config_object = None
current_mode = None
player = None

def play_media(file_path):
  if player != None: player.stop()
  player = vlc.MediaPlayer(file_path)
  player.play()

def handle_card_id(id):
  print('Pocessing...')
  if id not in config_object:
    # Make a beep
    print('\a \a \a')
    print("This card is not configured.")
  else:
    card_config = config_object[id]

    print(card_config["description"])

    # TODO: Have a batter config schema validation
    config_data = card_config.get("data")
    if config_data == None:
      # Make a beep
      print('\a \a \a')
      print("This card has no configuration data.")
      return

    card_type = card_config.get("type")
    if card_type == "mode":
      current_mode = config_data.get("default")
    elif card_type == 'media':
      media_file = config_data.get(current_mode)
      if media_file == None:
        media_file = config_data.get("default")

      play_media(media_file)

# Fetch the configs from a file
with open(CONFIG_FILE_NAME, 'r') as openfile:
  # Reading from json file
  config_object = json.load(openfile)

try:
  while True:
    try:
      print("Waiting to read a card...")

      id, text = reader.read()

      print("A card found: " + id)

      handle_card_id(id)
    except ValueError:
      print("Sorry, I didn't understand that.")
      # Better try again... Return to the start of the loop
      continue
finally:
  GPIO.cleanup()