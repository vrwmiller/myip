
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

# mytools

This repository provides a set of command-line tools for macOS, written in Python and shell script, to query public APIs and automate common tasks.

---

## Tools Overview

- **myip.py** — Get your public IPv4/IPv6 address and location info.
- **bandsintown.py** — Look up artist info and events from Bandsintown.
- **mediawiki.py** — Search Wikipedia and fetch page content.
- **stoic.py** — Display a random Stoic quote from stoic-quotes.com.
- **myopen.sh** — Launch multiple instances of a macOS application (where allowed).

---

## Requirements

- Python 3.7 or newer
- `requests` Python library

---

## Setup

Clone the repository and set up your environment:

```sh
git clone https://github.com/vrwmiller/myip.git
cd myip
source environment.sh
```

*If you already have the `requests` library installed globally, you can skip the virtual environment setup.*

---

## Usage

### myip.py

Get your public IP addresses and location:

```sh
python myip.py
```

**Example output:**

```text
MyIP.com: fd00::1 (United States, US)
ipify IPv4: 192.168.1.1
ipify IPv6: fd00::1
```

---

### bandsintown.py

Query artist info and events:

```sh
python bandsintown.py --app_id bandsintown@gmail.com --artist "tool"
```

**Example output:**

```text
Artist Info:
{ ...artist info JSON... }

Upcoming Events:
[{ ...event JSON... }, ...]
```

---

### mediawiki.py

Search Wikipedia or get page content:

```sh
python mediawiki.py --search "Python programming" --limit 2
python mediawiki.py --pageid 23862
```

**Example output:**

```text
Title: Python (programming language)
PageID: 23862
Snippet: ...

<page content>
```

---

### stoic.py

Show a random Stoic quote:

```sh
python stoic.py
```

**Example output:**

```text
"Waste no more time arguing what a good man should be. Be one."
-- Marcus Aurelius
```

---

### myopen.sh

Launch a new instance of a macOS application (including system apps, where possible):

```sh
myopen Calculator
myopen Safari
```

**Note:** Some system apps (like Calculator) may be restricted by macOS and may not allow multiple instances due to security constraints. This script checks both `/Applications` and `/System/Applications` for the app executable.

---

## License

MIT
