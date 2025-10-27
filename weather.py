import requests
import argparse

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
    for s in stations:
        props = s["properties"]
        lat = props.get('latitude', 'N/A')
        lon = props.get('longitude', 'N/A')
        print(f"{props['stationIdentifier']}: {props['name']} ({lat}, {lon})")

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
    parser.add_argument("--station", type=str, help="Station ID for current conditions (e.g., KJFK)")
    parser.add_argument("--list-stations", action="store_true", help="List stations for given lat/lon")
    args = parser.parse_args()

    if args.list_stations and args.lat is not None and args.lon is not None:
        _, _, _, stations_url = get_grid_points(args.lat, args.lon)
        print(f"Stations near ({args.lat}, {args.lon}):")
        list_stations(stations_url)
    elif args.lat is not None and args.lon is not None:
        grid_id, grid_x, grid_y, _ = get_grid_points(args.lat, args.lon)
        forecast = get_forecast(grid_id, grid_x, grid_y)
        print(f"Forecast for ({args.lat}, {args.lon}):")
        for period in forecast:
            print(f"{period['name']}: {period['detailedForecast']}")
    elif args.station:
        obs = get_station_observation(args.station)
        print(f"Current conditions at {args.station}:")
        temp_c = obs['temperature']['value']
        temp_f = temp_c * 9/5 + 32 if temp_c is not None else None
        if temp_c is not None:
            print(f"Temperature: {temp_c:.1f}°C / {temp_f:.1f}°F")
        else:
            print("Temperature: N/A")
        print(f"Wind: {obs['windDirection']['value']}° at {obs['windSpeed']['value']} m/s")
        print(f"Description: {obs['textDescription']}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
