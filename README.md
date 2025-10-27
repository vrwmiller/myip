
# mytools

This repository contains several Python command-line tools for querying public APIs and fetching useful information.

## Tools

- **myip.py**: Query your public IPv4 and IPv6 addresses using MyIP.com and ipify APIs.
- **bandsintown.py**: Query artist information and events using the Bandsintown Public API.
- **mediawiki.py**: Search Wikipedia and fetch page content using the MediaWiki Action API.
- **stoic.py**: Get a random Stoic quote from stoic-quotes.com API.
- **myopen.sh**: Launch multiple instances of a macOS application (including system apps, where possible).
---

### myopen.sh

Launch a new instance of a macOS application. Useful for apps that normally restrict to a single instance.

```sh
myopen Calculator
myopen Safari
```

Note: Some system apps (like Calculator) may be restricted by macOS and may not allow multiple instances due to security constraints.

---

---

## Requirements

- Python 3.7+
- `requests` library

---

## Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/vrwmiller/myip.git
    cd myip
    ```

2. Create and activate a virtual environment (recommended):

    ```sh
    source environment.sh
    ```

    **Note:** If you already have the `requests` library installed globally, you can skip the virtual environment setup and run the script directly.

---

## Usage

### myip.py

Shows your public IPv4 and IPv6 addresses, country, and country code.

```sh
python myip.py
```

Example output:

```
MyIP.com: fd00::1 (United States, US)
ipify IPv4: 192.168.1.1
ipify IPv6: fd00::1
```

---

### bandsintown.py

Fetches artist information and lists events (upcoming, past, or by date range).

```sh
python bandsintown.py --app_id bandsintown@gmail.com --artist "tool"
```

Example output:

```
Artist Info:
{ ...artist info JSON... }

Upcoming Events:
[{ ...event JSON... }, ...]
```

---

### mediawiki.py

Search Wikipedia or fetch page content.

```sh
python mediawiki.py --search "Python programming" --limit 2
python mediawiki.py --pageid 23862
```

Example output:

```
Title: Python (programming language)
PageID: 23862
Snippet: ...

<page content>
```

---

### stoic.py

Get a random Stoic quote.

```sh
python stoic.py
```

Example output:

```
"Waste no more time arguing what a good man should be. Be one."
-- Marcus Aurelius
```

---

## License

MIT
