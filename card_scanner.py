#!/usr/bin/env python

import json

CONFIG_FILE_NAME = "config.json"

config_object = None

# Fetch the configs from a file
with open(CONFIG_FILE_NAME, 'r') as openfile:
  # Reading from json file
  config_object = json.load(openfile)

while True:
  try:
    print("Please scan a card now, or 'Q' to exit:")
    # TODO: Add a line for reading the RFID card
    card_id = "1234"

    print("The card ID is: " + card_id)

    description = input("Please enter a short description to remember this ID, or 'Q' to exit: ")

    if description == "Q":
      break

    # Make sure the config key has an initialised empty dict value if it was new
    if card_id not in config_object:
      config_object[card_id] = {}

    config_object[card_id]["description"] = description
  except ValueError:
    print("Sorry, I didn't understand that.")
    # Better try again... Return to the start of the loop
    continue

print(config_object)

# Write the new config object to the config file
json_object = json.dumps(config_object, indent=2)
with open(CONFIG_FILE_NAME, "w") as outfile:
  outfile.write(json_object)
 
print("Config update is done! Goodbye.")