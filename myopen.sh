#!/bin/zsh
# Usage: ./myopen.sh <AppName>
# Example: ./myopen.sh Calculator

APP_NAME="$1"
APP_PATH="/Applications/$APP_NAME.app/Contents/MacOS/$APP_NAME"

if [ ! -x "$APP_PATH" ]; then
  echo "Cannot find executable for $APP_NAME at $APP_PATH"
  exit 1
fi

open -n "$APP_PATH" &
