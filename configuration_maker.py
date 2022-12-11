#!/usr/bin/env python

import json
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

CONFIG_FILE_NAME = "config.json"
config_object = None
reader = SimpleMFRC522()


def update_config():
  print('Saving new config file...')
  # Write the new config object to the config file
  json_object = json.dumps(config_object, indent=2)
  with open(CONFIG_FILE_NAME, "w") as outfile:
    outfile.write(json_object)
  print(config_object)


# Fetch the configs from a file
with open(CONFIG_FILE_NAME, 'r') as openfile:
  # Reading from json file
  config_object = json.load(openfile)

while True:
  try:
    description = input("Please enter a short description to remember the next card ID, or 'Q' to exit: ")

    if description == "Q":
      update_config()
      print("Config update is done! Goodbye.")
      exit(0)
      break

    print("Please scan the card now.")
    
    id, text = reader.read()
    print("The card ID is: " + str(id))

    # Make sure the config key has an initialised empty dict value if it was new
    if id not in config_object:
      config_object[id] = {}

    config_object[id]["description"] = description
    print('New card config saved!')
  except ValueError:
    print("Sorry, I didn't understand that.")
    # Better try again... Return to the start of the loop
    continue
  finally:
    GPIO.cleanup()
