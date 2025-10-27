
# mytools

This repository provides concise command-line tools for macOS, written in Python and shell script, to query public APIs and automate common tasks.

## Tools

- **myip.py** — Get your public IPv4/IPv6 address and location info.
- **bandsintown.py** — Look up artist info and events from Bandsintown.
- **mediawiki.py** — Search Wikipedia and fetch page content.
- **stoic.py** — Display a random Stoic quote from stoic-quotes.com.
- **myopen.sh** — Launch multiple instances of a macOS application (where allowed).
- **weather.py** — Get US National Weather Service forecasts and current conditions.
- **myopen.sh** — Launch multiple instances of a macOS application (where allowed).

## Requirements

- Python 3.7 or newer
- `requests` Python library

## Setup

Clone the repository and set up your environment:

```sh
git clone https://github.com/vrwmiller/myip.git
cd myip
source environment.sh
```

*If you already have the `requests` library installed globally, you can skip the virtual environment setup.*

## Usage

### weather.py

Get a forecast, current conditions, or list nearby stations by coordinates or city/state:

```sh
# By coordinates
python weather.py --lat 40.7128 --lon -74.0060           # Get forecast
python weather.py --station KJFK                         # Get current conditions
python weather.py --lat 40.7128 --lon -74.0060 --list-stations   # List stations near location

# By city and state
python weather.py --city "New York" --state NY           # Get forecast for New York, NY
python weather.py --city "New York" --state NY --list-stations   # List stations near New York, NY
```

### myip.py

```sh
python myip.py
```
Output:
```text
MyIP.com: fd00::1 (United States, US)
ipify IPv4: 192.168.1.1
ipify IPv6: fd00::1
```

### bandsintown.py

```sh
python bandsintown.py --app_id bandsintown@gmail.com --artist "tool"
```
Output:
```text
Artist Info:
{ ...artist info JSON... }

Upcoming Events:
[{ ...event JSON... }, ...]
```

### mediawiki.py

```sh
python mediawiki.py --search "Python programming" --limit 2
python mediawiki.py --pageid 23862
```
Output:
```text
Title: Python (programming language)
PageID: 23862
Snippet: ...

<page content>
```

### stoic.py

```sh
python stoic.py
```
Output:
```text
"Waste no more time arguing what a good man should be. Be one."
-- Marcus Aurelius
```

### myopen.sh

```sh
myopen Calculator
myopen Safari
```
Note: Some system apps (like Calculator) may be restricted by macOS and may not allow multiple instances due to security constraints. This script checks both `/Applications` and `/System/Applications` for the app executable.

## License

MIT
