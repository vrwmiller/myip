# myip

A simple Python script to query your public IPv4 and IPv6 addresses using MyIP.com and ipify APIs.

## Features
- Shows your public IPv4 and IPv6 addresses
- Displays country and country code (from MyIP.com)

## Requirements
- Python 3.7+
- `requests` library

## Setup
1. Clone the repository:
	```sh
	git clone https://github.com/vrwmiller/myip.git
	cd myip
	```
2. Create and activate a virtual environment:
	You can run the provided setup script:
	```sh
	source environment.sh
	```

## Usage
Run the script:
```sh
python myip.py
```

Example output:
```
MyIP.com: 2001:0db8:85a3:0000:0000:8a2e:0370:7334 (United States, US)
ipify IPv4: 203.0.113.42
ipify IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

## License
MIT
