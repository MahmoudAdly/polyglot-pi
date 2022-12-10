# polyglot-pi
A Raspberry Pi + RFID polyglot jukebox project.
The main idea is to make it possible for each RFID card to play different media files depending on the language (mode) set. This way, you can teach children multiple languages with less cards.

# How to use

## Step 1: Install all the python dependencies

```bash
sudo apt update
sudo apt upgrade

sudo apt install python3-dev python3-pip
sudo pip3 install spidev
sudo pip3 install mfrc522

sudo pip3 install python-vlc
```

## Step 2: Setup the config file and media files

To be able to play media files, you need to configure the app to identify each card and connect it to the media file(s) you want. This is done via [configuration_maker.py]. All you need to do is:
- Run this script.
- Scan each card and follow the instructions to give a short description to recognize the card ID in the config file later.
- Add your media files to the media folder and link each media file to the respective card config. Check [config.example.json] to understand how to build the config file correctly.

## Step 3: Run the main app

Now that your config file is ready and the media files are in place, you can run [app.py] to keep scanning new cards and playing their media files. This app needs to be run manually every time you start your Raspberry Pi. Alternatively, you can configure your Raspberry Pi to run this app on each boot.


