#!/bin/zsh
# Usage: ./myopen.sh <AppName>
# Example: ./myopen.sh Calculator


APP_NAME="$1"
APP_PATH="/Applications/$APP_NAME.app/Contents/MacOS/$APP_NAME"
SYS_APP_PATH="/System/Applications/$APP_NAME.app/Contents/MacOS/$APP_NAME"

if [ -x "$APP_PATH" ]; then
  open -n "$APP_PATH" &
elif [ -x "$SYS_APP_PATH" ]; then
  open -n "$SYS_APP_PATH" &
else
  echo "Cannot find executable for $APP_NAME at $APP_PATH or $SYS_APP_PATH"
  exit 1
fi
