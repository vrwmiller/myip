
# mytools project

This repository contains two Python scripts:

- `myip.py`: Query your public IPv4 and IPv6 addresses using MyIP.com and ipify APIs.
- `bandsintown.py`: Query artist information and events using the Bandsintown Public API.


## Features

### myip.py
- Shows your public IPv4 and IPv6 addresses
- Displays country and country code (from MyIP.com)

### bandsintown.py
- Fetches artist information (profile, photo, tracker count, etc.)
- Lists artist events (upcoming, past, or by date range)

## Requirements
- Python 3.7+
- `requests` library

## Setup
1. Clone the repository:
	```sh
	git clone https://github.com/vrwmiller/myip.git
	cd myip
	```
2. Create and activate a virtual environment (recommended):
	You can run the provided setup script:
	```sh
	source environment.sh
	```

	**Note:** If you already have the `requests` library installed globally, you can skip the virtual environment setup and run the script directly.


## Usage

### myip.py
Run the script:
```sh
python myip.py
```
Example output:
```
MyIP.com: fd00::1 (United States, US)
ipify IPv4: 192.168.1.1
ipify IPv6: fd00::1
```

### bandsintown.py
Set your Bandsintown `app_id` in the script, then run:
```sh
python bandsintown.py
```
Example output:
```
Artist Info:
{ ...artist info JSON... }

Upcoming Events:
[{ ...event JSON... }, ...]
```

## License
MIT
