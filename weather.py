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
    return grid_id, grid_x, grid_y

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
    parser.add_argument("--lat", type=float, help="Latitude for forecast")
    parser.add_argument("--lon", type=float, help="Longitude for forecast")
    parser.add_argument("--station", type=str, help="Station ID for current conditions (e.g., KJFK)")
    args = parser.parse_args()

    if args.lat is not None and args.lon is not None:
        grid_id, grid_x, grid_y = get_grid_points(args.lat, args.lon)
        forecast = get_forecast(grid_id, grid_x, grid_y)
        print(f"Forecast for ({args.lat}, {args.lon}):")
        for period in forecast:
            print(f"{period['name']}: {period['detailedForecast']}")
    elif args.station:
        obs = get_station_observation(args.station)
        print(f"Current conditions at {args.station}:")
        print(f"Temperature: {obs['temperature']['value']}°C")
        print(f"Wind: {obs['windDirection']['value']}° at {obs['windSpeed']['value']} m/s")
        print(f"Description: {obs['textDescription']}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
