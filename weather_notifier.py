from weather import get_coordinates, get_weather, is_raining, get_intermediate_points
import openrouteservice
from geopy.geocoders import Nominatim

# Replace with your OpenRouteService API key
ORS_API_KEY = '5b3ce3597851110001cf6248a48812f202544be4b3bc9ea2bb1dd71d'
client = openrouteservice.Client(key=ORS_API_KEY)

geolocator = Nominatim(user_agent="weather_notifier")

def get_waypoints(source, destination):
    try:
        source_coords = get_coordinates(source)
        dest_coords = get_coordinates(destination)

        route = client.directions(
            coordinates=[source_coords[::-1], dest_coords[::-1]],  # ORS requires (lon, lat)
            profile='driving-car',
            format='geojson'
        )

        waypoints = route['features'][0]['geometry']['coordinates']
        waypoints = [(lat, lon) for lon, lat in waypoints]
        return waypoints
    except Exception as e:
        raise Exception(f"Error fetching route data: {e}")

def get_place_name(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
        if location:
            address = location.raw.get('address', {})
            city = address.get('city', '')
            town = address.get('town', '')
            village = address.get('village', '')
            if city:
                return city
            elif town:
                return town
            elif village:
                return village
            else:
                return f"Latitude: {lat}, Longitude: {lon}"
        else:
            return f"Latitude: {lat}, Longitude: {lon}"
    except Exception as e:
        return f"Latitude: {lat}, Longitude: {lon}"

def get_weather_details(source, destination):
    try:
        waypoints = get_waypoints(source, destination)
        unique_places = set()
        results = []

        for lat, lon in waypoints:
            place_name = get_place_name(lat, lon)
            if place_name not in unique_places and place_name != f"Latitude: {lat}, Longitude: {lon}":
                unique_places.add(place_name)
                try:
                    weather = get_weather(lat, lon)
                    weather_description = weather['weather'][0]['description']
                    results.append({
                        'place': place_name,
                        'weather': weather_description,
                        'is_raining': is_raining(weather)
                    })
                except Exception as e:
                    results.append({
                        'place': place_name,
                        'weather': f"Could not retrieve weather: {e}",
                        'is_raining': False
                    })

        return results
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

if __name__ == "__main__":
    source = "Mysore"
    destination = "Mandya"
    weather_details = get_weather_details(source, destination)
    print(weather_details)
