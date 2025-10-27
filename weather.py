
import requests
import argparse
import shutil
import textwrap

def geocode_city_state(city, state):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "city": city,
        "state": state,
        "country": "USA",
        "format": "json",
        "limit": 1
    }
    r = requests.get(url, params=params, headers={"User-Agent": "weather.py (github.com/vrwmiller/mytools)"})
    r.raise_for_status()
    results = r.json()
    if results:
        lat = float(results[0]["lat"])
        lon = float(results[0]["lon"])
        return lat, lon
    else:
        raise ValueError(f"Could not geocode city/state: {city}, {state}")

BASE_URL = "https://api.weather.gov"

# Helper to get grid points for a location (lat, lon)
def get_grid_points(lat, lon):
    url = f"{BASE_URL}/points/{lat},{lon}"
    r = requests.get(url, headers={"User-Agent": "weather.py (github.com/vrwmiller/mytools)"})
    r.raise_for_status()
    data = r.json()
    grid_id = data["properties"]["gridId"]
    grid_x = data["properties"]["gridX"]
    grid_y = data["properties"]["gridY"]
    stations_url = data["properties"]["observationStations"]
    return grid_id, grid_x, grid_y, stations_url
def list_stations(stations_url):
    r = requests.get(stations_url, headers={"User-Agent": "weather.py (github.com/vrwmiller/mytools)"})
    r.raise_for_status()
    stations = r.json()["features"]
    width = shutil.get_terminal_size((80, 20)).columns
    for s in stations:
        props = s["properties"]
        lat = props.get('latitude', 'N/A')
        lon = props.get('longitude', 'N/A')
        line = f"{props['stationIdentifier']}: {props['name']} ({lat}, {lon})"
        print(textwrap.fill(line, width=width, subsequent_indent='    '))

# Get forecast for grid points
def get_forecast(grid_id, grid_x, grid_y):
    url = f"{BASE_URL}/gridpoints/{grid_id}/{grid_x},{grid_y}/forecast"
    r = requests.get(url, headers={"User-Agent": "weather.py (github.com/vrwmiller/mytools)"})
    r.raise_for_status()
    return r.json()["properties"]["periods"]

# Get current conditions for a station
def get_station_observation(station_id):
    url = f"{BASE_URL}/stations/{station_id}/observations/latest"
    r = requests.get(url, headers={"User-Agent": "weather.py (github.com/vrwmiller/mytools)"})
    r.raise_for_status()
    return r.json()["properties"]

def main():
    parser = argparse.ArgumentParser(description="Get weather info from the US National Weather Service API")
    parser.add_argument("--lat", type=float, help="Latitude for forecast or station list")
    parser.add_argument("--lon", type=float, help="Longitude for forecast or station list")
    parser.add_argument("--city", type=str, help="City for location lookup")
    parser.add_argument("--state", type=str, help="State for location lookup")
    parser.add_argument("--station", type=str, help="Station ID for current conditions (e.g., KJFK)")
    parser.add_argument("--list-stations", action="store_true", help="List stations for given location")
    args = parser.parse_args()

    lat, lon = args.lat, args.lon
    # If city/state provided, geocode to get lat/lon
    if args.city and args.state:
        try:
            lat, lon = geocode_city_state(args.city, args.state)
        except Exception as e:
            print(e)
            return

    if args.list_stations and lat is not None and lon is not None:
        _, _, _, stations_url = get_grid_points(lat, lon)
        print(f"Stations near ({lat}, {lon}):")
        list_stations(stations_url)
    elif lat is not None and lon is not None:
        grid_id, grid_x, grid_y, _ = get_grid_points(lat, lon)
        print(f"Forecast for ({lat}, {lon}):")
        forecast = get_forecast(grid_id, grid_x, grid_y)
        width = shutil.get_terminal_size((80, 20)).columns
        for period in forecast:
            line = f"{period['name']}: {period['detailedForecast']}"
            print(textwrap.fill(line, width=width, subsequent_indent='    '))
    elif args.station:
        obs = get_station_observation(args.station)
        print(f"Current conditions at {args.station}:")
        width = shutil.get_terminal_size((80, 20)).columns
        temp_c = obs['temperature']['value']
        temp_f = temp_c * 9/5 + 32 if temp_c is not None else None
        if temp_c is not None:
            line = f"Temperature: {temp_c:.1f}°C / {temp_f:.1f}°F"
            print(textwrap.fill(line, width=width, subsequent_indent='    '))
        else:
            print(textwrap.fill("Temperature: N/A", width=width, subsequent_indent='    '))
        wind_line = f"Wind: {obs['windDirection']['value']}° at {obs['windSpeed']['value']} m/s"
        print(textwrap.fill(wind_line, width=width, subsequent_indent='    '))
        desc_line = f"Description: {obs['textDescription']}"
        print(textwrap.fill(desc_line, width=width, subsequent_indent='    '))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
