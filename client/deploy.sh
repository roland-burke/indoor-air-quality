#!/bin/bash
TARGET=192.168.178.63
TARGET_PATH=/home/pi/air-quality-station/

echo "Deploying to $TARGET at $TARGET_PATH ..."
ssh pi@$TARGET "mkdir -p /home/pi/air-quality-station"
scp -r ./backend/* pi@$TARGET:$TARGET_PATH
echo "done"
