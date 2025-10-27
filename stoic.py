
import requests
import argparse
import shutil
import textwrap

API_URL = "https://stoic-quotes.com/api/quote"

def get_quote():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Get a random Stoic quote from stoic-quotes.com API.")
    args = parser.parse_args()
    quote = get_quote()
    width = shutil.get_terminal_size((80, 20)).columns
    wrapped_text = textwrap.fill(quote['text'], width=width)
    print(f"{wrapped_text}\n-- {quote['author']}")

if __name__ == "__main__":
    main()
