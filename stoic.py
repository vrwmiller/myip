import requests
import argparse

API_URL = "https://stoic-quotes.com/api/quote"

def get_quote():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Get a random Stoic quote from stoic-quotes.com API.")
    args = parser.parse_args()
    quote = get_quote()
    print(f"{quote['text']}\n-- {quote['author']}")

if __name__ == "__main__":
    main()
