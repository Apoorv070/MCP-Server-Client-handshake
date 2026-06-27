from __future__ import annotations

import math
from datetime import datetime


CITY_TO_IATA = {
    "london": "LON",
    "paris": "PAR",
    "berlin": "BER",
    "rome": "ROM",
    "madrid": "MAD",
    "barcelona": "BCN",
    "amsterdam": "AMS",
    "dublin": "DUB",
    "new york": "NYC",
    "san francisco": "SFO",
    "los angeles": "LAX",
    "chicago": "CHI",
    "miami": "MIA",
    "mumbai": "BOM",
    "delhi": "DEL",
    "bangalore": "BLR",
    "chennai": "MAA",
    "dubai": "DXB",
    "singapore": "SIN",
    "tokyo": "TYO",
    "sydney": "SYD",
    "toronto": "YTO",
    "vancouver": "YVR",
}

CITY_COORDS = {
    "london": (51.5074, -0.1278),
    "paris": (48.8566, 2.3522),
    "berlin": (52.52, 13.405),
    "rome": (41.9028, 12.4964),
    "madrid": (40.4168, -3.7038),
    "barcelona": (41.3874, 2.1686),
    "amsterdam": (52.3676, 4.9041),
    "dublin": (53.3498, -6.2603),
    "new york": (40.7128, -74.006),
    "san francisco": (37.7749, -122.4194),
    "los angeles": (34.0522, -118.2437),
    "chicago": (41.8781, -87.6298),
    "miami": (25.7617, -80.1918),
    "mumbai": (19.076, 72.8777),
    "delhi": (28.6139, 77.209),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "dubai": (25.2048, 55.2708),
    "singapore": (1.3521, 103.8198),
    "tokyo": (35.6762, 139.6503),
    "sydney": (-33.8688, 151.2093),
    "toronto": (43.6532, -79.3832),
    "vancouver": (49.2827, -123.1207),
}

IATA_TO_CITY = {code: city.title() for city, code in CITY_TO_IATA.items()}
IATA_TO_CITY["ROM"] = "Rome"
IATA_TO_CITY["TYO"] = "Tokyo"
IATA_TO_CITY["YTO"] = "Toronto"
IATA_TO_CITY["CHI"] = "Chicago"
IATA_TO_CITY["NYC"] = "New York"
IATA_TO_CITY["LON"] = "London"
IATA_TO_CITY["PAR"] = "Paris"

COUNTRY_DATA = {
    "france": {
        "country": "France",
        "region": "Europe",
        "currencies": "Euro (EUR)",
        "coordinates": [46.2276, 2.2137],
    },
    "india": {
        "country": "India",
        "region": "Asia",
        "currencies": "Indian rupee (INR)",
        "coordinates": [20.5937, 78.9629],
    },
    "united kingdom": {
        "country": "United Kingdom",
        "region": "Europe",
        "currencies": "Pound sterling (GBP)",
        "coordinates": [55.3781, -3.436],
    },
    "united states": {
        "country": "United States",
        "region": "North America",
        "currencies": "United States dollar (USD)",
        "coordinates": [39.8283, -98.5795],
    },
    "italy": {
        "country": "Italy",
        "region": "Europe",
        "currencies": "Euro (EUR)",
        "coordinates": [41.8719, 12.5674],
    },
    "germany": {
        "country": "Germany",
        "region": "Europe",
        "currencies": "Euro (EUR)",
        "coordinates": [51.1657, 10.4515],
    },
    "spain": {
        "country": "Spain",
        "region": "Europe",
        "currencies": "Euro (EUR)",
        "coordinates": [40.4637, -3.7492],
    },
    "united arab emirates": {
        "country": "United Arab Emirates",
        "region": "Asia",
        "currencies": "UAE dirham (AED)",
        "coordinates": [23.4241, 53.8478],
    },
    "japan": {
        "country": "Japan",
        "region": "Asia",
        "currencies": "Japanese yen (JPY)",
        "coordinates": [36.2048, 138.2529],
    },
    "singapore": {
        "country": "Singapore",
        "region": "Asia",
        "currencies": "Singapore dollar (SGD)",
        "coordinates": [1.3521, 103.8198],
    },
    "canada": {
        "country": "Canada",
        "region": "North America",
        "currencies": "Canadian dollar (CAD)",
        "coordinates": [56.1304, -106.3468],
    },
    "australia": {
        "country": "Australia",
        "region": "Oceania",
        "currencies": "Australian dollar (AUD)",
        "coordinates": [-25.2744, 133.7751],
    },
}

HOTELS_BY_CITY = {
    "paris": [
        ("Grand Paris Residence", "PAR101", 48.8578, 2.3514),
        ("Seine View Hotel", "PAR102", 48.8601, 2.3376),
        ("Left Bank Suites", "PAR103", 48.8491, 2.343),
        ("Montmartre Stay", "PAR104", 48.8867, 2.3431),
        ("Louvre Garden Inn", "PAR105", 48.8648, 2.3346),
    ],
    "london": [
        ("Thames Central Hotel", "LON101", 51.5079, -0.1287),
        ("Covent Garden Rooms", "LON102", 51.5117, -0.124),
        ("Paddington Suites", "LON103", 51.5154, -0.1754),
        ("South Bank Lodge", "LON104", 51.5052, -0.1167),
        ("Kensington Court Hotel", "LON105", 51.4999, -0.1936),
    ],
    "dubai": [
        ("Marina Palm Resort", "DXB101", 25.0816, 55.1362),
        ("Downtown Dunes Hotel", "DXB102", 25.1975, 55.2744),
        ("Creekside Business Inn", "DXB103", 25.2565, 55.3054),
        ("Desert Pearl Suites", "DXB104", 25.2043, 55.2701),
        ("Jumeirah Breeze Hotel", "DXB105", 25.2091, 55.2477),
    ],
}

WEATHER_PROFILES = [
    ("Clear sky", 28.0),
    ("Partly cloudy", 24.0),
    ("Light rain", 22.0),
    ("Sunny", 30.0),
    ("Overcast", 20.0),
]


def get_iata_code(city_name: str) -> str | None:
    clean_name = city_name.strip().lower()
    if len(clean_name) == 3:
        return clean_name.upper()
    return CITY_TO_IATA.get(clean_name)


def fetch_country_info_data(country_name: str):
    key = country_name.strip().lower()
    info = COUNTRY_DATA.get(key)
    if not info:
        return f"Error: Could not find a country named '{country_name}'."
    return info


def _distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_km * c


def _city_coords_from_code_or_name(value: str) -> tuple[float, float] | None:
    clean = value.strip().lower()
    if clean in CITY_COORDS:
        return CITY_COORDS[clean]
    if len(clean) == 3:
        for city, code in CITY_TO_IATA.items():
            if code.lower() == clean:
                return CITY_COORDS.get(city)
    return None


def search_cheap_flights_data(origin_city: str, max_price: int) -> str:
    origin_code = get_iata_code(origin_city)
    if not origin_code:
        return f"Error: I don't know the IATA code for '{origin_city}'."

    origin_coords = _city_coords_from_code_or_name(origin_city)
    if not origin_coords:
        return f"Error: I don't know the IATA code for '{origin_city}'."

    options = []
    for city, code in CITY_TO_IATA.items():
        if code == origin_code:
            continue
        coords = CITY_COORDS.get(city)
        if not coords:
            continue
        dist = _distance_km(origin_coords[0], origin_coords[1], coords[0], coords[1])
        est_price = int(45 + dist * 0.08)
        if est_price <= max_price:
            month = (abs(hash(origin_code + code)) % 9) + 1
            day = (abs(hash(code + origin_code)) % 20) + 10
            options.append((est_price, code, f"2026-{month:02d}-{day:02d}"))

    if not options:
        return f"No flights found from {origin_city} under {max_price} EUR."

    options.sort(key=lambda item: (item[0], item[1]))
    return "\n".join(
        f"- To {code} on {date}: EUR {price}" for price, code, date in options[:5]
    )


def search_specific_flights_data(origin_city: str, destination_city: str, date: str) -> str:
    origin_code = get_iata_code(origin_city)
    dest_code = get_iata_code(destination_city)
    if not origin_code:
        return f"Error: Unknown city '{origin_city}'."
    if not dest_code:
        return f"Error: Unknown city '{destination_city}'."

    try:
        travel_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return "Request Failed: time data does not match format 'YYYY-MM-DD'"

    if travel_date < datetime.now().date():
        return "No flights found."

    origin_coords = _city_coords_from_code_or_name(origin_city)
    dest_coords = _city_coords_from_code_or_name(destination_city)
    dist = _distance_km(origin_coords[0], origin_coords[1], dest_coords[0], dest_coords[1])
    base_price = 60 + dist * 0.09
    duration_hours = max(1.2, dist / 780)

    carriers = ["AI", "BA", "EK", "LH", "SQ"]
    offers = []
    for idx, carrier in enumerate(carriers):
        depart_hour = 6 + idx * 3
        depart_min = 15 if idx % 2 == 0 else 45
        arrival_total_hours = depart_hour + depart_min / 60 + duration_hours + idx * 0.15
        arr_hour = int(arrival_total_hours) % 24
        arr_min = int(round((arrival_total_hours % 1) * 60)) % 60
        price = round(base_price + idx * 18 + (travel_date.day % 7) * 6, 2)
        offers.append(
            f"- EUR {price:.2f}: {depart_hour:02d}:{depart_min:02d}-{arr_hour:02d}:{arr_min:02d} ({carrier})"
        )
    return "\n".join(offers[:5])


def find_hotels_data(city_name: str) -> str:
    city_code = get_iata_code(city_name)
    if not city_code:
        return f"Error: Unknown city '{city_name}'."

    hotels = HOTELS_BY_CITY.get(city_name.strip().lower())
    if not hotels:
        coords = _city_coords_from_code_or_name(city_name)
        if not coords:
            return f"No hotels found in {city_name}."
        hotels = []
        city_title = city_name.strip().title()
        for idx in range(5):
            lat = coords[0] + (idx - 2) * 0.01
            lon = coords[1] + (2 - idx) * 0.01
            hotels.append(
                (f"{city_title} Stay {idx + 1}", f"{city_code}{idx + 101}", lat, lon)
            )

    return "\n".join(
        f"- {name} (ID: {hotel_id}) at [{lat}, {lon}]"
        for name, hotel_id, lat, lon in hotels[:5]
    )


def get_coordinates_data(place_name: str):
    clean = place_name.strip().lower()
    coords = CITY_COORDS.get(clean)
    if not coords:
        for city, city_coords in CITY_COORDS.items():
            if city in clean or clean in city:
                coords = city_coords
                break
    if not coords:
        return f"Could not find coordinates for '{place_name}'."
    return {"latitude": coords[0], "longitude": coords[1], "name": place_name}


def get_driving_distance_data(lat1: float, lon1: float, lat2: float, lon2: float) -> str:
    dist_km = _distance_km(lat1, lon1, lat2, lon2) * 1.22
    duration_min = (dist_km / 48) * 60
    return f"{dist_km:.2f} km, {duration_min:.0f} mins"


def get_weather_data(lat: float, lon: float) -> str:
    seed = int(abs(lat * 10) + abs(lon * 10))
    label, base_temp = WEATHER_PROFILES[seed % len(WEATHER_PROFILES)]
    temp = base_temp - abs(lat) * 0.03 + (abs(lon) % 7) * 0.2
    return f"{label}, {temp:.1f}°C"
