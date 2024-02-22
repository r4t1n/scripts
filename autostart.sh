#!/bin/bash

solaar --window=hide
sleep 10 # asusctl needs the asusd daemon to start
asusctl profile --profile-set Quiet
