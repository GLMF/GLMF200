#!/bin/bash

KEYBOARD='Logitech USB Keyboard'
MOUSE='Logitech G500'

# Get ${KEYBOARD} id
id=`xinput --list | grep "${KEYBOARD}" | head -n1 | cut -f2 | cut -d= -f2`

# Get ${KEYBOARD} Node Device
device=`xinput --list-props ${id} | grep 'Device Node' | cut -f3 | sed 's/"//g'`

# Disable ${KEYBOARD}
xinput --set-prop ${id} "Device Enabled" 0


# Get ${MOUSE} id
id_mouse=`xinput --list | grep "${MOUSE}" | head -n1 | cut -f2 | cut -d= -f2`

# Get ${MOUSE} Node Device
device_mouse=`xinput --list-props ${id_mouse} | grep 'Device Node' | cut -f3 | sed 's/"//g'`


# Python script call
python3 keyboard.py ${device} ${device_mouse}
