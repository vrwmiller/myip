
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

Output (forecast):
```text
Forecast for (40.7128, -74.0060):
Tonight: Mostly clear, with a low around 55. Northwest wind 5 to 7 mph.
Monday: Sunny, with a high near 70. North wind 3 to 6 mph.
...etc...
```

Output (current conditions):
```text
Current conditions at KJFK:
Temperature: 18°C / 64°F
Wind: 270° at 5 m/s
Description: Partly Cloudy
```

Output (station list):
```text
Stations near (40.7128, -74.0060):
KNYC: Central Park (40.782, -73.965)
KJFK: John F Kennedy International Airport (40.6398, -73.7789)
...etc...
```

## Requirements

- Python 3.7 or newer

# mytools

Command-line tools for macOS to query public APIs and automate common tasks.

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

## Tools

- **myip.py** — Get your public IPv4/IPv6 address and location info.
- **bandsintown.py** — Look up artist info and events from Bandsintown.
- **mediawiki.py** — Search Wikipedia and fetch page content.
- **stoic.py** — Display a random Stoic quote from stoic-quotes.com.
- **weather.py** — Get US National Weather Service forecasts, current conditions, and list stations by coordinates or city/state.
- **myopen.sh** — Launch multiple instances of a macOS application (where allowed).

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
