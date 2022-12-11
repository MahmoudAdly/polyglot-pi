#!/usr/bin/env python

import json
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import vlc

reader = SimpleMFRC522()
CONFIG_FILE_NAME = "config.json"
config_object = None
current_mode = None
last_card_id = None
player = None

def beep():
  print('\a \a \a')

def play_media(file_path):
  if player != None: player.stop()
  player = vlc.MediaPlayer(file_path)
  player.play()

def handle_card_id(id):
  print('Pocessing card ID...')
  if id not in config_object:
    # Make a beep
    beep()
    print("This card ID is not recognized. Please add it to the config file.")
    return

  card_config = config_object[id]

  print(card_config["description"])

  # TODO: Have a batter config schema validation
  config_data = card_config.get("data")

  if config_data == None:
    beep()
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
  elif card_type == 'action':
    beep()
    print('Action cards are not supported yet.')

# Step 1: Fetch the configs from a json file
with open(CONFIG_FILE_NAME, 'r') as openfile:
  config_object = json.load(openfile)

# Step 2: Read any given card in a loop
try:
  while True:
    try:
      print("Waiting for a card to read...")

      id, text = reader.read()

      id_str = str(id)
      print("A card found. ID: " + id_str)

      if id == last_card_id:
        print('Same card was found. Waiting for a new card.')
      else:
        last_card_id = id_str
        handle_card_id(id_str)
    except ValueError:
      print("Sorry, I didn't understand that.")
      # Better try again... Return to the start of the loop
      continue
finally:
  GPIO.cleanup()