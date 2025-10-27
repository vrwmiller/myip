import requests
import argparse

BASE_URL = "https://rest.bandsintown.com"

class BandsintownAPI:
    def __init__(self, app_id):
        self.app_id = app_id

    def get_artist_info(self, artist_name):
        url = f"{BASE_URL}/artists/{artist_name}"
        params = {"app_id": self.app_id}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_artist_events(self, artist_name, date=None):
        url = f"{BASE_URL}/artists/{artist_name}/events"
        params = {"app_id": self.app_id}
        if date:
            params["date"] = date  # e.g., "upcoming", "past", "all", or "YYYY-MM-DD,YYYY-MM-DD"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_venue_events(self, venue_name, location=None):
        # Bandsintown API does not provide a direct venue search endpoint in public docs,
        # but you can filter artist events by venue name.
        # This function will search all events for a venue name match (client-side filter).
        raise NotImplementedError("Venue search is not directly supported by Bandsintown Public API.")

def main():
    parser = argparse.ArgumentParser(description="Bandsintown API CLI")
    parser.add_argument("--app_id", required=True, help="Bandsintown app_id")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--artist", help="Artist name to search")
    group.add_argument("--venue", help="Venue name to search (not directly supported)")
    parser.add_argument("--events", action="store_true", help="Show events for artist or venue")
    parser.add_argument("--date", help="Date filter for events (upcoming, past, all, or YYYY-MM-DD,YYYY-MM-DD)")
    args = parser.parse_args()

    api = BandsintownAPI(args.app_id)

    if args.artist:
        if args.events:
            events = api.get_artist_events(args.artist, date=args.date)
            print(f"Events for artist '{args.artist}':")
            print(events)
        else:
            info = api.get_artist_info(args.artist)
            print(f"Info for artist '{args.artist}':")
            print(info)
    elif args.venue:
        print("Venue search is not directly supported by Bandsintown Public API.")
        # You could implement a workaround by searching all artist events for a venue match.

if __name__ == "__main__":
    main()
