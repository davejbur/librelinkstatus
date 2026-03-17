# LibreLink Status Display

## Overview

This is a simple idea to try and use the [PyLibreLinkUp](https://github.com/robberwick/pylibrelinkup) library to display the patient's current glucose value on screen.

For me, I can keep an eye on my close relative's glucose levels whilst at my laptop by quickly alt-tabbing to the window, rather than having to unlock my phone & find the app.

The next stage will be to get it running on a Raspberry Pi, and have it sitting in a corner of the kitchen...

(You will already need to have created a [LibreLinkUp](https://librelinkup.com/) account, and the patient will need to have shared their data with you.)

## Usage

1. Install Python (if you haven't already)
2. Install PyLibreLinkUp
```
pip install pylibrelinkup
```
3. Rename ``defaultconfig.ini`` to ``config.ini``
4. Edit ``config.ini``: change ``llusername`` to the email address you used in your LibreLinkUp account, and save
4. Run it
```
python main.py
```

If you are behind a proxy server, remember to set them either in the code or in environment settings.
