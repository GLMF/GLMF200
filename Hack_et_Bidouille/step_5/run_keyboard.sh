#!/bin/bash

KEYBOARD='Logitech USB Keyboard'

# Get ${KEYBOARD} id
id=`xinput --list | grep "${KEYBOARD}" | head -n1 | cut -f2 | cut -d= -f2`

# Get ${KEYBOARD} Node Device
device=`xinput --list-props ${id} | grep 'Device Node' | cut -f3 | sed 's/"//g'`

# Disable ${KEYBOARD}
xinput --set-prop ${id} "Device Enabled" 0

# Python script call
python3 keyboard.py ${device}
