"""
Supervisor Agent

The main orchestrating agent that coordinates specialized subagents
to create comprehensive travel plans.

This implements the SubAgents pattern where:
- Supervisor receives user requests and makes routing decisions
- Subagents are wrapped as tools for the supervisor to call
- Results flow back to supervisor for synthesis
"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from subagents import (
    create_flights_agent,
    create_hotels_agent,
    create_activities_agent,
    create_itinerary_agent,
)

_agents = None

def initialize_agents(model_name: str = "openai:gpt-4o-mini"):

    """Initialize the model and all subagents"""
    model = init_chat_model(model_name)

    return {
        "model": model,
        "flights_agent": create_flights_agent(model),
        "hotels_agent": create_hotels_agent(model),
        "activities_agent": create_activities_agent(model),
        "itinerary_agent": create_itinerary_agent(model),
    }

def get_agents():
    """Get or initialize agents"""
    global _agents
    if _agents is None:
        _agents = initialize_agents()

    return _agents

# Wrap Each SubAgent in a Tool

@tool
def search_flights(request: str) -> str:
    """Search for flights to a destination.
    
    Use this when the user needs to find flights. Pass the full context including:
    - Destination city
    - Travel dates (if mentioned)
    - Budget constraints (if mentioned)
    - Preferences (direct flights, specific airlines, etc.)
    
    Example: "Find flights to Tokyo, budget around $800, prefer direct flights"
    """

    agents = get_agents()

    result = agents["flights_agent"].invoke({
        "messages": [{"role": "user", "content": request}]
    })

    return result["messages"][-1].text

@tool
def search_hotels(request: str) -> str:
    """Search for hotels and accommodations.
    
    Use this when the user needs to find places to stay. Pass the full context including:
    - Destination city
    - Traveler type (solo, couple, family, etc.)
    - Budget per night (if mentioned)
    - Preferences (amenities, location, etc.)
    
    Example: "Find family-friendly hotels in Tokyo, budget $200/night, need pool"
    """
    agents = get_agents()
    result = agents["hotels_agent"].invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text

@tool
def search_activities(request: str) -> str:
    """Search for things to do, attractions, and restaurants.
    
    Use this when the user wants to discover activities, experiences, or dining options. 
    Pass the full context including:
    - Destination city
    - Interests (culture, food, nature, adventure, etc.)
    - Trip style (relaxed, packed, foodie, etc.)
    - Any specific requests
    
    Example: "Find cultural activities and good sushi restaurants in Tokyo"
    """
    agents = get_agents()
    result = agents["activities_agent"].invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text

@tool
def create_itinerary(request: str) -> str:
    """Create and organize a trip itinerary.
    
    Use this to organize flights, hotels, and activities into a cohesive plan.
    Pass the full context including:
    - All selected components (flight, hotel, activities)
    - Number of days
    - Trip pace preference (relaxed, moderate, packed)
    - Any scheduling preferences
    
    Example: "Create a 5-day Tokyo itinerary with the selected hotel and activities"
    """
    agents = get_agents()
    result = agents["itinerary_agent"].invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text


SUPERVISOR_PROMPT = """You are a professional travel planning assistant. Your job is to help users plan their perfect trip by coordinating specialized travel experts.

You have access to four specialist tools:
1. search_flights - Find and compare flight options
2. search_hotels - Find accommodations matching preferences  
3. search_activities - Discover things to do, attractions, and restaurants
4. create_itinerary - Organize everything into a day-by-day plan

WORKFLOW GUIDELINES:

For a complete trip planning request:
1. First, understand the user's needs (destination, dates, travelers, budget, interests)
2. Search for flights to get travel options
3. Search for hotels matching their traveler type and budget
4. Search for activities based on their interests
5. Create an itinerary to organize everything

For partial requests (e.g., "just find hotels"):
- Only call the relevant specialist
- Don't overwhelm with unnecessary information

RESPONSE GUIDELINES:

- Be conversational and helpful, not robotic
- Summarize key findings clearly
- Make specific recommendations when you have enough information
- Ask clarifying questions if the request is vague
- Present options in a scannable format
- Always consider the user's budget and preferences

When synthesizing results from multiple specialists:
- Use the create_itinerary tool to format and display your final result
- Highlight the best matches for their needs
- Note any trade-offs they should consider
- Provide a cohesive recommendation, not just raw data

Remember: You're a knowledgeable travel advisor, not just a search engine. 
Add value by making thoughtful recommendations based on the user's specific situation."""


def create_supervisor_agent(
        model_name: str = "openai:gpt-4o-mini",
        use_memory: bool = True
    ):
    """Create and return the supervisor agent.
    
    Args:
        model_name: The model to use for the supervisor
        use_memory: Whether to enable conversation memory (checkpointing)
    
    Returns:
        Configured supervisor agent
    """

    global _agents
    _agents = initialize_agents(model_name)

    supervisor = create_agent(
        _agents["model"],
        tools=[search_flights, search_hotels, search_activities, create_itinerary],
        system_prompt=SUPERVISOR_PROMPT,
        checkpointer = InMemorySaver() if use_memory else None
    )

    return supervisor

