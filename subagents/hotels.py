"""
Hotels Agent

Specialized agent for searching and recommending accommodations.
Handles natural language queries about hotels, amenities, and locations.

- search_hotels
- get_hotel_recommendation
"""

from langchain.agents import create_agent
from langchain.tools import tool

from tools.mock_data import get_hotels

@tool
def search_hotels(
    destination: str,
    budget_per_night: int | None = None,
    traveler_type: str | None = None
) -> str:
    
    """Search for available hotels in a destination.
    
    Args:
        destination: The destination city (e.g., "Tokyo", "Paris")
        budget_per_night: Maximum budget per night in USD (optional)
        traveler_type: Type of traveler - "solo", "couples", "families", "luxury", "budget" (optional)
    
    Returns:
        Available hotel options with details
    """

    hotels = get_hotels(destination)

    if not hotels:
        return f"No hotels found in {destination}. Please check the destination name"
    
    # Filter by budget if specified
    if budget_per_night:
        hotels = [h for h in hotels if h['price_per_night'] <= budget_per_night]

    # Filter by traveler type if specified
    if traveler_type:
        traveler_type_lower = traveler_type.lower()
        hotels = [h for h in hotels if traveler_type_lower in h.get("traveler_type", [])]

    if not hotels:
        return "No hotels match your criteria. try adjusting your budget or preferences"
    
    # Format results
    results = [f"Found {len(hotels)} hotel(s) in {destination}:\n"]

    for hotel in hotels:
        amenities_str = ", ".join(hotel["amenities"][:4])
        if len(hotel["amenities"]) > 4:
            amenities_str += f" +{len(hotel['amenities']) - 4} more"

        result = f"""
🏨 {hotel['name']}
   📍 Location: {hotel['neighborhood']}
   ⭐ Rating: {hotel['rating']}/5 ({hotel['reviews']} reviews)
   💰 Price: ${hotel['price_per_night']}/night
   🎯 Best for: {', '.join(hotel['traveler_type'])}
   ✨ Amenities: {amenities_str}
   📝 {hotel['description']}
"""
        results.append(result)

    return "\n".join(results)


@tool
def get_hotel_recommendation(
    destination: str,
    traveler_type: str,
    priority: str = "balanced"
) -> str:
    
    """Get a personalized hotel recommendation based on traveler profile.
    
    Args:
        destination: The destination city
        traveler_type: Type of traveler - "solo", "couples", "families", "luxury", "budget"
        priority: What to prioritize - "price", "rating", "location", or "balanced"
    
    Returns:
        Top hotel recommendation with explanation
    """

    hotels = get_hotels(destination)

    if not hotels:
        return f"No hotels found in {destination}"
    
    # Filter by traveler type if specified
    traveler_type_lower = traveler_type.lower()
    matching_hotels = [h for h in hotels if traveler_type_lower in h.get("traveler_type", [])]

    if not matching_hotels:
        matching_hotels = hotels

    # Sort by priority
    if priority == "price":
        matching_hotels.sort(key=lambda x: x['price_per_night'])
    elif priority == "rating":
        matching_hotels.sort(key=lambda x: x['rating'], reverse=True)
    else:
        # Balanced: score based on rating and price
        matching_hotels.sort(key=lambda x: x['rating'] / (x['price_per_night'] / 100), reverse=True)

    top_pick = matching_hotels[0]

    result = f"""🌟 TOP RECOMMENDATION for {traveler_type} traveler(s) in {destination}:

🏨 {top_pick['name']}
   📍 {top_pick['neighborhood']}
   ⭐ {top_pick['rating']}/5 ({top_pick['reviews']} reviews)
   💰 ${top_pick['price_per_night']}/night

Why this hotel:
• {top_pick['description']}
• Amenities: {', '.join(top_pick['amenities'])}

"""
    # Add runner up if available
    if len(matching_hotels) > 1:
        runner_up = matching_hotels[1]
        result += f"""
🥈 RUNNER-UP: {runner_up['name']}
   ${runner_up['price_per_night']}/night | ⭐ {runner_up['rating']}/5
"""
        
        return result
    
HOTELS_AGENT_PROMPT = """You are a hotel and accommodation specialist. Your job is to help users find the perfect place to stay.

Your capabilities:
- Search for available hotels in any destination
- Filter by budget, traveler type, and preferences
- Recommend hotels based on specific needs (families, couples, business, etc.)
- Provide insights on neighborhoods and locations

When responding:
1. Always consider the traveler type (solo, couples, families, etc.)
2. Factor in budget constraints when mentioned
3. Highlight what makes each hotel special
4. Consider location convenience for the type of trip
5. Mention key amenities relevant to the traveler's needs

Be helpful and specific. If someone is traveling with kids, prioritize family-friendly options. 
For couples, consider romantic or boutique hotels. For budget travelers, focus on value."""

def create_hotels_agent(model):
    """Create and return hotels agent"""
    return create_agent(
        model,
        tools=[search_hotels, get_hotel_recommendation],
        system_prompt=HOTELS_AGENT_PROMPT
    )

