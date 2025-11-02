## Requirements

- Python 3.7 or newer
- `requests` Python library

## Setup

Clone the repository and set up your environment:

```sh
git clone https://github.com/vrwmiller/mytools.git
cd mytools
python3 -m venv venv
source environment.sh
```

<details>
<summary><strong>bible-verse.py - Get Bible verses</strong></summary>

**Usage:**

```sh
bible-verse                # Get a random verse from Psalms
bible-verse --verse "John 3:16"   # Get a specific verse
bible-verse --translation ESV      # Specify translation
bible-verse --format json          # Output as JSON
```

**Options:**

- `--verse` Specify verse reference (e.g. "John 3:16")
- `--translation` Bible translation (default: KJV)
- `--output-file` Write verse to file
- `--format` Output format: text (default) or json

**Output:**

- Text: `REFERENCE: Verse text`
- JSON: Full API response

</details>
<details>
<summary><strong>trello.py - Search Trello cards</strong></summary>

**Usage:**

```sh
trello.py --board BOARD_ID --name "*deploy to prod*" --format json --output-file results.json
```

**Options:**

- `--board` Board ID
- `--list` List ID
- `--member` Member ID
- `--name` Card name pattern (wildcards supported)
- `--log-file` Log file path (default: trello.py.log)
- `--debug` Enable debug logging to STDOUT
- `--max-results` Page size (not used, for compatibility)
- `--output-file` Write results to file
- `--format` Output format: text (default) or json
- `--config` Path to config file (default: ~/.trello.cfg)

**Config file (~/.trello.cfg):**

```
[trello]
key = YOUR_API_KEY
token = YOUR_API_TOKEN
default_board = BOARD_ID
```

**Security:**

- Protect your config file: `chmod 600 ~/.trello.cfg`
- API token is never logged (redacted in logs)

**Output:**

- Text: `CARD_ID — Card Name` (one per line)
- JSON: Array of objects `{ "id": ..., "name": ... }`

</details>
<details>
<summary><strong>jira.py - Search Jira issues</strong></summary>

**Usage:**

```sh
jira.py --project ABC --summary "*deploy to prod*" --format json --output-file results.json
```

**Options:**

- `--project` Project key (e.g. ABC)
- `--reporter` Reporter username
- `--summary` Summary pattern (wildcards supported)
- `--log-file` Log file path (default: jira.py.log)
- `--debug` Enable debug logging to STDOUT
- `--max-results` Page size (maxResults per request)
- `--output-file` Write results to file
- `--format` Output format: text (default) or json
- `--config` Path to config file (default: ~/.jira.cfg)

**Config file (~/.jira.cfg):**

```
[jira]
url = https://your.jira.instance
token = YOUR_ACCESS_TOKEN
default_project = ABC
```

**Security:**

- Protect your config file: `chmod 600 ~/.jira.cfg`
- Access token is never logged (redacted in logs)

**Output:**

- Text: `KEY — Summary` (one per line)
- JSON: Array of objects `{ "key": ..., "summary": ... }`

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
  python randomstr.py                # Default: 32 chars
  python randomstr.py --length 16    # Specify length (12-64)
  python randomstr.py --exclude "abc" # Exclude characters
  randomstr --length 20 --exclude "!@#" # Using alias
  ```

  Output:

  ```text
  Generated random string: 8f$Gz@1!kL... (example)
  ```

</details>

<details>
  <summary><strong>randomstr.sh Usage</strong></summary>

  Generate a random string with optional length and excluded characters:

  ```sh
  ./randomstr.sh                # Default: 32 chars
  ./randomstr.sh -l 16          # Specify length (12-64)
  ./randomstr.sh -e "abc"       # Exclude characters
  randomstrsh -l 20 -e "!@#"    # Using alias
  ```

  Output:

  ```text
  Generated random string: 8f$Gz@1!kL... (example)
  ```

</details>

<details>
  <summary><strong>csvtransform.py Usage</strong></summary>

  Transform a CSV file by rearranging columns and separating debit/credit amounts:

  ```sh
  python csvtransform.py -i input.csv -o output.csv
  python csvtransform.py --input input.csv --output output.csv
  csvtransform -i input.csv -o output.csv   # Using alias
  ```

  Output:

  ```text
  Transformed data has been written to output.csv
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

<details>
  <summary><strong>Testing with pytest</strong></summary>

  To run all tests for the project:

  ```sh
  # (Recommended) Ensure dependencies are installed
  pip install -r requirements.txt

  # Run all tests in the tests/ directory
  pytest tests/
  # Or, if using a virtual environment:
  ./venv/bin/python -m pytest tests/
  ```

- All test files are located in the `tests/` directory.
- Tests cover core functions, edge cases, and integration logic.
- Mocking is used for Google Sheets and file I/O where needed.
- For coverage reporting, install `pytest-cov` and run:

    ```sh
    pytest --cov=csvimport tests/
    ```

</details>
