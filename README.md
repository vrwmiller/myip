## Requirements
- Python 3.7 or newer
- `requests` Python library
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

<details>
  <summary><strong>weather.py Usage</strong></summary>

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
  <summary><strong>myopen.sh Usage</strong></summary>

  ```sh
  myopen Calculator
  myopen Safari
  ```
  Note: Some system apps (like Calculator) may be restricted by macOS and may not allow multiple instances due to security constraints. This script checks both `/Applications` and `/System/Applications` for the app executable.
</details>
