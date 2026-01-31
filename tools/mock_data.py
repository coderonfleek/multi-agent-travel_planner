"""
Mock Travel Data

Realistic travel data for demonstration purposes.
In production, these would be replaced with actual API calls to:
- Amadeus, Skyscanner, Google Flights (flights)
- Booking.com, Hotels.com, Airbnb (hotels)
- TripAdvisor, Viator, GetYourGuide (activities)
"""

# =============================================================================
# FLIGHT DATA
# =============================================================================

MOCK_FLIGHTS = {
    "tokyo": [
        {
            "id": "FL001",
            "airline": "Japan Airlines",
            "flight_number": "JL005",
            "departure_city": "Los Angeles",
            "arrival_city": "Tokyo Narita",
            "departure_time": "11:30",
            "arrival_time": "15:30+1",
            "duration": "12h 00m",
            "stops": 0,
            "class": "Economy",
            "price": 850,
            "currency": "USD",
        },
        {
            "id": "FL002",
            "airline": "ANA",
            "flight_number": "NH105",
            "departure_city": "Los Angeles",
            "arrival_city": "Tokyo Haneda",
            "departure_time": "13:45",
            "arrival_time": "17:45+1",
            "duration": "12h 00m",
            "stops": 0,
            "class": "Economy",
            "price": 920,
            "currency": "USD",
        },
        {
            "id": "FL003",
            "airline": "United Airlines",
            "flight_number": "UA839",
            "departure_city": "Los Angeles",
            "arrival_city": "Tokyo Narita",
            "departure_time": "10:00",
            "arrival_time": "14:15+1",
            "duration": "12h 15m",
            "stops": 0,
            "class": "Economy",
            "price": 780,
            "currency": "USD",
        },
        {
            "id": "FL004",
            "airline": "Korean Air",
            "flight_number": "KE012",
            "departure_city": "Los Angeles",
            "arrival_city": "Tokyo Narita",
            "departure_time": "09:30",
            "arrival_time": "18:45+1",
            "duration": "17h 15m",
            "stops": 1,
            "layover": "Seoul (2h 30m)",
            "class": "Economy",
            "price": 650,
            "currency": "USD",
        },
    ],
    "paris": [
        {
            "id": "FL005",
            "airline": "Air France",
            "flight_number": "AF065",
            "departure_city": "New York JFK",
            "arrival_city": "Paris CDG",
            "departure_time": "19:00",
            "arrival_time": "08:30+1",
            "duration": "7h 30m",
            "stops": 0,
            "class": "Economy",
            "price": 650,
            "currency": "USD",
        },
        {
            "id": "FL006",
            "airline": "Delta",
            "flight_number": "DL264",
            "departure_city": "New York JFK",
            "arrival_city": "Paris CDG",
            "departure_time": "22:30",
            "arrival_time": "12:00+1",
            "duration": "7h 30m",
            "stops": 0,
            "class": "Economy",
            "price": 580,
            "currency": "USD",
        },
    ],
}


# =============================================================================
# HOTEL DATA
# =============================================================================

MOCK_HOTELS = {
    "tokyo": [
        {
            "id": "HT001",
            "name": "Park Hyatt Tokyo",
            "neighborhood": "Shinjuku",
            "rating": 4.8,
            "reviews": 2847,
            "price_per_night": 450,
            "currency": "USD",
            "amenities": ["Spa", "Pool", "Gym", "Restaurant", "Bar", "Room Service"],
            "description": "Luxury hotel featured in 'Lost in Translation'. Stunning views of Mt. Fuji and Tokyo skyline.",
            "traveler_type": ["couples", "luxury", "business"],
        },
        {
            "id": "HT002",
            "name": "Shinjuku Granbell Hotel",
            "neighborhood": "Shinjuku",
            "rating": 4.3,
            "reviews": 1523,
            "price_per_night": 120,
            "currency": "USD",
            "amenities": ["Restaurant", "Bar", "Free WiFi", "Laundry"],
            "description": "Modern boutique hotel in the heart of Shinjuku. Walking distance to station and nightlife.",
            "traveler_type": ["solo", "couples", "budget"],
        },
        {
            "id": "HT003",
            "name": "Hilton Tokyo Bay",
            "neighborhood": "Maihama (Disney Area)",
            "rating": 4.4,
            "reviews": 3201,
            "price_per_night": 200,
            "currency": "USD",
            "amenities": ["Pool", "Gym", "Kids Club", "Restaurant", "Disney Shuttle"],
            "description": "Family-friendly hotel with direct access to Tokyo Disney Resort. Great for families with children.",
            "traveler_type": ["families", "kids"],
        },
        {
            "id": "HT004",
            "name": "The Peninsula Tokyo",
            "neighborhood": "Marunouchi",
            "rating": 4.9,
            "reviews": 1876,
            "price_per_night": 600,
            "currency": "USD",
            "amenities": ["Spa", "Pool", "Gym", "Multiple Restaurants", "Limousine Service"],
            "description": "Ultra-luxury hotel near Imperial Palace. Exceptional service and elegant rooms.",
            "traveler_type": ["luxury", "couples", "business"],
        },
        {
            "id": "HT005",
            "name": "MIMARU Tokyo Shinjuku",
            "neighborhood": "Shinjuku",
            "rating": 4.5,
            "reviews": 892,
            "price_per_night": 180,
            "currency": "USD",
            "amenities": ["Kitchen", "Washer", "Free WiFi", "Living Area"],
            "description": "Apartment-style hotel perfect for families. Full kitchen and spacious rooms.",
            "traveler_type": ["families", "groups", "long-stay"],
        },
    ],
    "paris": [
        {
            "id": "HT006",
            "name": "Le Meurice",
            "neighborhood": "1st Arrondissement",
            "rating": 4.9,
            "reviews": 1245,
            "price_per_night": 800,
            "currency": "USD",
            "amenities": ["Spa", "Michelin Restaurant", "Gym", "Concierge"],
            "description": "Palace hotel overlooking Tuileries Garden. Salvador Dalí's favorite Paris hotel.",
            "traveler_type": ["luxury", "couples"],
        },
        {
            "id": "HT007",
            "name": "Hotel Fabric",
            "neighborhood": "11th Arrondissement",
            "rating": 4.4,
            "reviews": 987,
            "price_per_night": 150,
            "currency": "USD",
            "amenities": ["Free WiFi", "Bar", "Courtyard"],
            "description": "Boutique hotel in a converted textile factory. Trendy Oberkampf neighborhood.",
            "traveler_type": ["couples", "solo", "budget"],
        },
    ],
}


# =============================================================================
# ACTIVITIES DATA
# =============================================================================

MOCK_ACTIVITIES = {
    "tokyo": [
        # Cultural
        {
            "id": "AC001",
            "name": "Senso-ji Temple & Asakusa Walking Tour",
            "category": "Culture",
            "duration": "3 hours",
            "price": 45,
            "currency": "USD",
            "rating": 4.7,
            "description": "Explore Tokyo's oldest temple and the traditional Asakusa district with a local guide.",
            "best_for": ["culture", "history", "photography"],
            "location": "Asakusa",
        },
        {
            "id": "AC002",
            "name": "Meiji Shrine & Harajuku Tour",
            "category": "Culture",
            "duration": "2.5 hours",
            "price": 35,
            "currency": "USD",
            "rating": 4.6,
            "description": "Visit the serene Meiji Shrine then explore quirky Harajuku fashion district.",
            "best_for": ["culture", "shopping", "youth"],
            "location": "Harajuku",
        },
        {
            "id": "AC003",
            "name": "Imperial Palace East Gardens",
            "category": "Culture",
            "duration": "1.5 hours",
            "price": 0,
            "currency": "USD",
            "rating": 4.4,
            "description": "Free entry to beautiful gardens on former Edo Castle grounds.",
            "best_for": ["culture", "nature", "budget"],
            "location": "Marunouchi",
        },
        # Food
        {
            "id": "AC004",
            "name": "Tsukiji Outer Market Food Tour",
            "category": "Food",
            "duration": "3 hours",
            "price": 80,
            "currency": "USD",
            "rating": 4.9,
            "description": "Taste fresh sushi, tamagoyaki, and street food at Tokyo's famous fish market area.",
            "best_for": ["food", "culture", "morning"],
            "location": "Tsukiji",
        },
        {
            "id": "AC005",
            "name": "Ramen Tasting Tour in Shinjuku",
            "category": "Food",
            "duration": "2.5 hours",
            "price": 65,
            "currency": "USD",
            "rating": 4.8,
            "description": "Sample different styles of ramen from 3 top-rated shops with a local foodie.",
            "best_for": ["food", "nightlife"],
            "location": "Shinjuku",
        },
        {
            "id": "AC006",
            "name": "Cooking Class: Sushi & Bento Making",
            "category": "Food",
            "duration": "3 hours",
            "price": 95,
            "currency": "USD",
            "rating": 4.8,
            "description": "Learn to make sushi rolls and traditional bento boxes with a professional chef.",
            "best_for": ["food", "culture", "families"],
            "location": "Ginza",
        },
        # Entertainment
        {
            "id": "AC007",
            "name": "Tokyo DisneySea",
            "category": "Entertainment",
            "duration": "Full day",
            "price": 75,
            "currency": "USD",
            "rating": 4.9,
            "description": "World-renowned theme park with unique nautical themes. Best Disney park globally.",
            "best_for": ["families", "entertainment", "kids"],
            "location": "Maihama",
        },
        {
            "id": "AC008",
            "name": "teamLab Borderless Digital Art Museum",
            "category": "Entertainment",
            "duration": "2-3 hours",
            "price": 30,
            "currency": "USD",
            "rating": 4.7,
            "description": "Immersive digital art experience with stunning interactive installations.",
            "best_for": ["art", "photography", "unique"],
            "location": "Odaiba",
        },
        {
            "id": "AC009",
            "name": "Robot Restaurant Show",
            "category": "Entertainment",
            "duration": "1.5 hours",
            "price": 80,
            "currency": "USD",
            "rating": 4.2,
            "description": "Wild, over-the-top robot cabaret show. Quintessential quirky Tokyo experience.",
            "best_for": ["nightlife", "unique", "entertainment"],
            "location": "Shinjuku",
        },
        # Nature & Views
        {
            "id": "AC010",
            "name": "Mt. Fuji Day Trip",
            "category": "Nature",
            "duration": "10-12 hours",
            "price": 120,
            "currency": "USD",
            "rating": 4.6,
            "description": "Visit Mt. Fuji 5th Station, Oshino Hakkai, and enjoy stunning views.",
            "best_for": ["nature", "photography", "day-trip"],
            "location": "Day trip from Tokyo",
        },
        {
            "id": "AC011",
            "name": "Tokyo Skytree Observation Deck",
            "category": "Views",
            "duration": "1-2 hours",
            "price": 20,
            "currency": "USD",
            "rating": 4.5,
            "description": "Panoramic views from the world's tallest tower. Best at sunset.",
            "best_for": ["views", "photography", "evening"],
            "location": "Sumida",
        },
    ],
    "paris": [
        {
            "id": "AC012",
            "name": "Louvre Museum Guided Tour",
            "category": "Culture",
            "duration": "3 hours",
            "price": 65,
            "currency": "USD",
            "rating": 4.8,
            "description": "Skip-the-line tour of world's largest art museum. See Mona Lisa and Venus de Milo.",
            "best_for": ["culture", "art", "history"],
            "location": "1st Arrondissement",
        },
        {
            "id": "AC013",
            "name": "Eiffel Tower Summit Access",
            "category": "Views",
            "duration": "2 hours",
            "price": 45,
            "currency": "USD",
            "rating": 4.7,
            "description": "Skip-the-line access to the summit of Paris's iconic landmark.",
            "best_for": ["views", "photography", "romantic"],
            "location": "7th Arrondissement",
        },
    ],
}


# =============================================================================
# RESTAURANTS DATA
# =============================================================================

MOCK_RESTAURANTS = {
    "tokyo": [
        {
            "id": "RS001",
            "name": "Sukiyabashi Jiro",
            "cuisine": "Sushi",
            "price_range": "$$$$",
            "rating": 4.9,
            "neighborhood": "Ginza",
            "description": "Legendary 3-Michelin star sushi. Reservation required months in advance.",
            "best_for": ["special occasion", "sushi lovers"],
        },
        {
            "id": "RS002",
            "name": "Ichiran Shibuya",
            "cuisine": "Ramen",
            "price_range": "$",
            "rating": 4.5,
            "neighborhood": "Shibuya",
            "description": "Famous tonkotsu ramen chain with private booth seating. No reservations needed.",
            "best_for": ["solo dining", "late night", "budget"],
        },
        {
            "id": "RS003",
            "name": "Gonpachi Nishi-Azabu",
            "cuisine": "Japanese",
            "price_range": "$$",
            "rating": 4.4,
            "neighborhood": "Roppongi",
            "description": "The 'Kill Bill' restaurant. Traditional izakaya with soba and yakitori.",
            "best_for": ["groups", "atmosphere", "tourists"],
        },
        {
            "id": "RS004",
            "name": "Afuri Ramen",
            "cuisine": "Ramen",
            "price_range": "$",
            "rating": 4.6,
            "neighborhood": "Ebisu",
            "description": "Light, refreshing yuzu shio ramen. Modern, casual atmosphere.",
            "best_for": ["lunch", "healthy", "quick meal"],
        },
        {
            "id": "RS005",
            "name": "Narisawa",
            "cuisine": "Innovative Japanese",
            "price_range": "$$$$",
            "rating": 4.8,
            "neighborhood": "Aoyama",
            "description": "2-Michelin star innovative cuisine. 'Satoyama' concept celebrating Japanese nature.",
            "best_for": ["fine dining", "special occasion", "foodies"],
        },
    ],
}


def get_flights(destination: str) -> list:
    """Get available flights for a destination"""
    return MOCK_FLIGHTS.get(destination.lower(), [])

def get_hotels(destination: str) -> list:
    """Get available hotels for a destination"""
    return MOCK_HOTELS.get(destination.lower(), [])

def get_activities(destination: str) -> list:
    """Get available activities for a destination"""
    return MOCK_ACTIVITIES.get(destination.lower(), [])

def get_restaurants(destination: str) -> list:
    """Get restaurant recommendations for a destination"""
    return MOCK_RESTAURANTS.get(destination.lower(), [])

