try:
    from langchain_core.tools import tool
except ImportError:
    class _LocalTool:
        def __init__(self, func):
            self.func = func
            self.__name__ = getattr(func, "__name__", "tool")
            self.__doc__ = getattr(func, "__doc__", None)

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

        def invoke(self, values):
            return self.func(**values)

    def tool(func):
        return _LocalTool(func)

from internal_tools import (
    fetch_country_info_data,
    find_hotels_data,
    get_coordinates_data,
    get_driving_distance_data,
    get_weather_data,
    search_cheap_flights_data,
    search_specific_flights_data,
)


@tool
def fetch_country_info(country_name: str):
    """
    Fetches broad details about a country.

    WHEN TO USE:
    Use this when the user asks generic questions about a destination's region, currency, or language.

    ARGS:
        country_name (str): The full English name of the country (e.g., "France", "India").

    RETURNS:
        dict: A dictionary with the following keys:
              - 'country': (str) Common name of the country.
              - 'region': (str) Geographic region (e.g., 'Europe').
              - 'currencies': (str) A string listing currency names and codes.
              - 'coordinates': (list) [latitude, longitude] of the country center.
    """
    return fetch_country_info_data(country_name)


@tool
def search_cheap_flights(origin_city: str, max_price: int):
    """
    Finds ANY flight destinations from an origin city that fit within a budget.

    WHEN TO USE:
    Use this when the user is "Open Ended" (e.g., "Where can I go from London for $200?").
    DO NOT use this if the user specified a destination (use 'search_specific_flights' instead).

    ARGS:
        origin_city (str): The name of the city you are leaving from (e.g., 'Paris').
        max_price (int): The maximum budget in EUR.

    RETURNS:
        str: A newline-separated string where each line is a flight option.
             Format: "- To {Destination Code} on {Date}: EUR {Price}"
    """
    return search_cheap_flights_data(origin_city, max_price)


@tool
def search_specific_flights(origin_city: str, destination_city: str, date: str):
    """
    Finds flights between two specific cities on a specific date.

    WHEN TO USE:
    Use this when the user gives a concrete plan (Origin -> Destination + Date).

    ARGS:
        origin_city (str): Departure city name (e.g., 'London').
        destination_city (str): Arrival city name (e.g., 'New York').
        date (str): The date of travel in 'YYYY-MM-DD' format. MUST be a future date.

    RETURNS:
        str: A newline-separated string detailing specific flight offers.
             Format: "- EUR {Price}: {Time} -> {Time} ({Airline})"
    """
    return search_specific_flights_data(origin_city, destination_city, date)


@tool
def find_hotels(city_name: str):
    """
    Finds a list of hotels located in a specific city.

    WHEN TO USE:
    Use this to find accommodation options after a destination is selected.

    ARGS:
        city_name (str): The city name to search in (e.g., 'Paris').

    RETURNS:
        str: A newline-separated string list of hotels.
             Format: "- {Hotel Name} (ID: {ID}) at [{Lat}, {Lon}]"
    """
    return find_hotels_data(city_name)


@tool
def get_coordinates(place_name: str):
    """
    Converts a place name (city, landmark, or address) into GPS coordinates.

    WHEN TO USE:
    CRITICAL: You MUST use this tool BEFORE calling 'get_weather' or 'get_driving_distance'.
    Those tools require 'lat' and 'lon', and this tool provides them.

    ARGS:
        place_name (str): The name of the place (e.g., "Eiffel Tower", "New York City").

    RETURNS:
        dict: A dictionary with keys:
              - 'latitude': (float) The latitude.
              - 'longitude': (float) The longitude.
              - 'name': (str) The full resolved name of the place.
    """
    return get_coordinates_data(place_name)


@tool
def get_driving_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    """
    Calculates the driving distance and duration between two GPS points.

    DEPENDENCIES:
    You CANNOT call this with city names. You MUST run 'get_coordinates' first
    to get the (lat, lon) for both Start and End points.

    ARGS:
        lat1, lon1: Start point coordinates (float).
        lat2, lon2: End point coordinates (float).

    RETURNS:
        str: A string describing the route.
             Format: "{Distance} km, {Time} mins"
    """
    return get_driving_distance_data(lat1, lon1, lat2, lon2)


@tool
def get_weather(lat: float, lon: float):
    """
    Fetches the current weather for a specific GPS location.

    DEPENDENCIES:
    You MUST call 'get_coordinates' or 'find_hotels' first to get the Latitude/Longitude.
    Do NOT guess the coordinates.

    ARGS:
        lat (float): Latitude.
        lon (float): Longitude.

    RETURNS:
        str: A concise weather report.
             Format: "{Condition}, {Temperature}°C"
    """
    return get_weather_data(lat, lon)
