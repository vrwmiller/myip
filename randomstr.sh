#!/bin/zsh
# Usage: ./randomstr.sh [-l length] [-e exclude]
# Default length: 32, min: 12, max: 64

length=32
exclude=""

while getopts "l:e:" opt; do
  case $opt in
    l) length=$OPTARG ;;
    e) exclude=$OPTARG ;;
    *) echo "Usage: $0 [-l length] [-e exclude]"; exit 1 ;;
  esac
done

if [[ $length -lt 12 || $length -gt 64 ]]; then
  echo "Length must be between 12 and 64."
  exit 1
fi

# Build character set
all_chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_\`{|}~"
for (( i=0; i<${#exclude}; i++ )); do
  char="${exclude:$i:1}"
  all_chars="${all_chars//$char/}"
done

if [[ -z "$all_chars" ]]; then
  echo "All characters are excluded, cannot generate a random string."
  exit 1
fi

result=""
for (( i=0; i<$length; i++ )); do
  idx=$(( RANDOM % ${#all_chars} ))
  result+="${all_chars:$idx:1}"
done

echo "Generated random string: $result"
