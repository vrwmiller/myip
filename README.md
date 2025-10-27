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
2. Create and activate a virtual environment (recommended):
	You can run the provided setup script:
	```sh
	source environment.sh
	```

	**Note:** If you already have the `requests` library installed globally, you can skip the virtual environment setup and run the script directly.

## Usage
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

## License
MIT
