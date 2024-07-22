import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Replace with your actual API key
WEATHER_API_KEY = '05361d86fc24612a00581544122977ef'

def get_coordinates(location):
    geolocator = Nominatim(user_agent="weather_notifier")
    try:
        location_info = geolocator.geocode(location, timeout=10)
        if location_info:
            return (location_info.latitude, location_info.longitude)
        else:
            raise ValueError(f"Could not get coordinates for {location}")
    except Exception as e:
        raise Exception(f"Error getting coordinates for {location}: {e}")

def get_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        response.raise_for_status()

def is_raining(weather_data):
    weather_conditions = weather_data.get('weather', [])
    for condition in weather_conditions:
        if 'rain' in condition['main'].lower():
            return True
    return False

def get_intermediate_points(start, end, num_points=5):
    start_lat, start_lon = start
    end_lat, end_lon = end
    points = []
    for i in range(num_points):
        ratio = i / (num_points - 1)
        lat = start_lat + ratio * (end_lat - start_lat)
        lon = start_lon + ratio * (end_lon - start_lon)
        points.append((lat, lon))
    return points

def main():
    try:
        source = input("Enter the source location: ")
        destination = input("Enter the destination location: ")

        source_lat, source_lon = get_coordinates(source)
        dest_lat, dest_lon = get_coordinates(destination)

        source_weather = get_weather(source_lat, source_lon)
        dest_weather = get_weather(dest_lat, dest_lon)

        print(f"Weather at source ({source}): {source_weather['weather'][0]['description']}")
        print(f"Weather at destination ({destination}): {dest_weather['weather'][0]['description']}")

        if is_raining(source_weather):
            print(f"It's raining at the source ({source}).")
        else:
            print(f"It's not raining at the source ({source}).")

        if is_raining(dest_weather):
            print(f"It's raining at the destination ({destination}).")
        else:
            print(f"It's not raining at the destination ({destination}).")

        # Get weather for intermediate points
        intermediate_points = get_intermediate_points((source_lat, source_lon), (dest_lat, dest_lon), num_points=3)
        for i, (lat, lon) in enumerate(intermediate_points, start=1):
            weather = get_weather(lat, lon)
            print(f"Weather at intermediate point {i} ({lat}, {lon}): {weather['weather'][0]['description']}")
            if is_raining(weather):
                print(f"It's raining at intermediate point {i}.")
            else:
                print(f"It's not raining at intermediate point {i}.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
