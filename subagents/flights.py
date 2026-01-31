"""
Specialized for searching and recommending flights

It handles natural language queries about flight options, prices, and schedules

- search_flights
- compare_flight_prices
"""

from langchain.agents import create_agent
from langchain.tools import tool

from tools.mock_data import get_flights

@tool
def search_flights(
        destination: str,
        budget_max: int | None = None,
        preferred_stops: str = "any"
) -> str: 
    """Search for available flights to a destination.
    
    Args:
        destination: The destination city (e.g., "Tokyo", "Paris")
        budget_max: Maximum budget per person in USD (optional)
        preferred_stops: "direct", "one-stop", or "any"
    
    Returns:
        Available flight options with details
    """

    flights = get_flights(destination)

    if not flights:
        return f"No flights found to {destination}. Please check the destination name."
    
    # Filter By budget if specified
    if budget_max:
        flights = [f for f in flights if f["price"] <= budget_max]

    # Filter by stops if specified
    if preferred_stops == "direct":
        flights = [f for f in flights if f["stops"] == 0]
    elif preferred_stops == "one-stop":
        flights = [f for f in flights if f["stops"] == 1]

    if not flights:
        return "No flights match your criteria. Try adjusting your budget or stop preferences"
    
    # Format and Build Results
    results = [f"Found {len(flights)} flight(s) to {destination}:\n"]

    for flight in flights:
        result = f"""
* {flight['airline']} {flight['flight_number']}
  Route: {flight['departure_city']} -> {flight['arrival_city']}
  Depature: {flight['departure_time']} | Arrival: {flight['arrival_time']}
  Duration: {flight['duration']} | Stops: {flight['stops']} {'('+ flight.get('layover', '') + ')' if flight.get('layover') else '(Direct)'}
  Price: ${flight['price']} USD ({flight['class']})
"""
        results.append(result)

    return "\n".join(results)

@tool
def compare_flight_prices(destination: str) -> str:
    """Compare prices across all available flights to a destination.
    
    Args:
        destination: The destination city
    
    Returns:
        Price comparison summary with cheapest and recommended options
    """

    flights = get_flights(destination)

    if not flights:
        return f"No flights found to {destination}"
    
    # Sort by price
    sorted_flights = sorted(flights, key=lambda x: x['price'])
    cheapest = sorted_flights[0]

    # Find the best value (direct flght with good price)
    direct_flights = [f for f in flights if f["stops"] == 0]
    best_value = min(direct_flights, key=lambda x: x['price']) if direct_flights else cheapest

    result = f"""Flight Price Comparison to {destination}:

💰 CHEAPEST OPTION:
   {cheapest['airline']} {cheapest['flight_number']} - ${cheapest['price']}
   {cheapest['duration']} | {'Direct' if cheapest['stops'] == 0 else f"{cheapest['stops']} stop(s)"}

⭐ BEST VALUE (Direct):
   {best_value['airline']} {best_value['flight_number']} - ${best_value['price']}
   {best_value['duration']} | Direct flight

📊 Price Range: ${sorted_flights[0]['price']} - ${sorted_flights[-1]['price']}
"""
    
    return result

FLIGHTS_AGENT_PROMPT = """You are a flight search specialist. Your job is to help users find the best flights for their trip.

Your capabilities:
- Search for available flights to any destination
- Compare prices across different airlines
- Filter by budget, number of stops, and preferences
- Recommend the best options based on user needs

When responding:
1. Always search for flights first using the search_flights tool
2. Consider the user's budget constraints if mentioned
3. Highlight the trade-offs between price, duration, and convenience
4. Recommend specific flights based on the user's priorities (cheapest, fastest, most convenient)

Be concise but informative. Focus on actionable recommendations."""

def create_flights_agent(model):
    """Create and return the flight agent"""
    return create_agent(
        model,
        tools=[search_flights, compare_flight_prices],
        system_prompt=FLIGHTS_AGENT_PROMPT
    )

