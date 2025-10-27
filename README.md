## Requirements
- Python 3.7 or newer
- `requests` Python library

## Setup

Clone the repository and set up your environment:

```sh
git clone https://github.com/vrwmiller/myip.git
cd mytools
source environment.sh
```

*If you already have the `requests` library installed globally, you can skip the virtual environment setup.*

## Usage

<details>
  <summary><strong>weather.py Usage</strong></summary>

  Get a forecast, current conditions, or list nearby stations by coordinates or city/state:

  ```sh
  # By coordinates (default: 1 day, use --days 1-10 for more)
  python weather.py --lat 40.7128 --lon -74.0060                 # Get 1-day forecast
  python weather.py --lat 40.7128 --lon -74.0060 --days 5        # Get 5-day forecast
  python weather.py --station KJFK                               # Get current conditions
  python weather.py --lat 40.7128 --lon -74.0060 --list-stations # List stations near location

  # By city and state
  python weather.py --city "New York" --state NY                 # Get 1-day forecast for New York, NY
  python weather.py --city "New York" --state NY --days 7        # Get 7-day forecast for New York, NY
  python weather.py --city "New York" --state NY --list-stations # List stations near New York, NY
  ```
  
  - The `--days` option controls the number of days in the forecast (default: 1, min: 1, max: 10).
</details>

<details>
  <summary><strong>myip.py Usage</strong></summary>

  ```sh
  python myip.py
  ```
  Output:
  ```text
  MyIP.com: fd00::1 (United States, US)
  ipify IPv4: 192.168.1.1
  ipify IPv6: fd00::1
  ```
</details>

<details>
  <summary><strong>bandsintown.py Usage</strong></summary>

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
</details>

<details>
  <summary><strong>mediawiki.py Usage</strong></summary>

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
</details>

<details>
  <summary><strong>stoic.py Usage</strong></summary>

  ```sh
  python stoic.py
  ```
  Output:
  ```text
  "Waste no more time arguing what a good man should be. Be one."
  -- Marcus Aurelius
  ```
</details>

<details>
  <summary><strong>randomstr.py Usage</strong></summary>

  Generate a random string with optional length and excluded characters:

  ```sh
  python randomstr.py                # Default: 24 chars
  python randomstr.py --length 16    # Specify length (12-32)
  python randomstr.py --exclude "abc" # Exclude characters
  random --length 20 --exclude "!@#" # Using alias
  ```
  Output:
  ```text
  Generated random string: 8f$Gz@1!kL... (example)
  ```
</details>

<details>
  <summary><strong>myopen.sh Usage</strong></summary>

  ```sh
  myopen Calculator
  myopen Safari
  ```
  Note: Some system apps (like Calculator) may be restricted by macOS and may not allow multiple instances due to security constraints. This script checks both `/Applications` and `/System/Applications` for the app executable.
</details>
