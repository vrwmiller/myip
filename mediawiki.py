import requests
import argparse

API_ENDPOINT = "https://en.wikipedia.org/w/api.php"

def search_wikipedia(query, limit=1):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": limit
    }
    response = requests.get(API_ENDPOINT, params=params)
    response.raise_for_status()
    return response.json()["query"]["search"]

def get_page_content(pageid):
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "pageids": pageid,
        "format": "json"
    }
    response = requests.get(API_ENDPOINT, params=params)
    response.raise_for_status()
    pages = response.json()["query"]["pages"]
    return pages[str(pageid)]["extract"]

def main():
    parser = argparse.ArgumentParser(description="MediaWiki API client")
    parser.add_argument("--search", type=str, help="Search Wikipedia for a query")
    parser.add_argument("--limit", type=int, default=1, help="Number of search results")
    parser.add_argument("--pageid", type=int, help="Get content for a specific pageid")
    args = parser.parse_args()

    if args.search:
        results = search_wikipedia(args.search, args.limit)
        for result in results:
            print(f"Title: {result['title']}")
            print(f"PageID: {result['pageid']}")
            print(f"Snippet: {result['snippet']}")
            print()
    if args.pageid:
        content = get_page_content(args.pageid)
        print(content)

if __name__ == "__main__":
    main()
