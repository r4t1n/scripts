#!/bin/bash
asusctl profile --next
notify-send "ASUS Profile" "$(asusctl profile --profile-get)"
