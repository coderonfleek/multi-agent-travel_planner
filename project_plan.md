# 🌏 Smart Travel Planner - Project Plan

> **Multi-Agent Travel Planning System using the SubAgents Pattern**
>
> LangChain / LangGraph Implementation

---

## 📋 Project Overview

The **Smart Travel Planner** is a multi-agent system that helps users create comprehensive trip itineraries through natural conversation. Users describe their trip requirements, and the system coordinates multiple specialized agents to deliver a complete travel plan.

### The User Experience

A user might say:

> *"Plan a 5-day trip to Tokyo for me and my wife. We love food and culture. Mid-range budget, around $3000 total."*

The system then:

1. Finds suitable flight options
2. Recommends hotels matching their traveler profile
3. Discovers activities aligned with their interests (food, culture)
4. Organizes everything into a logical day-by-day itinerary
5. Presents a cohesive travel plan with specific recommendations

### Input & Output

| Input                                | Output                           |
| ------------------------------------ | -------------------------------- |
| Destination                          | Flight recommendations           |
| Travel dates                         | Hotel recommendations            |
| Number of travelers                  | Curated activities & restaurants |
| Traveler type (couple, family, solo) | Day-by-day itinerary             |
| Budget                               | Budget breakdown                 |
| Interests & preferences              | Practical travel tips            |

---

## 🎯 Why SubAgents Pattern?

### Requirements Analysis

| Requirement                         | Description                                                                  |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| **Multiple Domains**          | Flights, hotels, activities, itinerary planning are distinct specializations |
| **Centralized Orchestration** | Need one coordinator to manage the planning workflow                         |
| **User Interaction**          | User should talk to one consistent "travel advisor" persona                  |
| **Context Isolation**         | Each domain search should be focused, not polluted by other domains          |
| **Sequential Dependencies**   | Itinerary planning needs results from other searches first                   |
| **Synthesis Required**        | Final output must weave all components into cohesive plan                    |

### Pattern Evaluation

| Pattern             | Verdict | Reasoning                                                                                              |
| ------------------- | ------- | ------------------------------------------------------------------------------------------------------ |
| **Handoffs**  | ❌      | Sequential transfers feel bureaucratic. No parallelism. Users don't need to "talk" to each department. |
| **Skills**    | ❌      | Shared context causes bloat. Tool overload risk. Weak isolation between domains.                       |
| **Router**    | ⚠️    | Stateless by default. Poor for follow-up questions. Travel planning is conversational.                 |
| **SubAgents** | ✅      | Perfect fit! Centralized control, conversational, isolated contexts, natural synthesis.                |

### Why SubAgents Wins

**✅ Advantages:**

* User talks to one "travel advisor" throughout
* Supervisor handles dynamic orchestration
* Natural synthesis of all results
* Conversation continuity for follow-ups
* Focused context per specialist
* Parallel execution possible

**⚠️ Accepted Tradeoffs:**

* Extra LLM call for supervisor synthesis
* Slightly higher latency than single agent
* More complex architecture
* Subagents can't talk to user directly

### The Deciding Factors

```
┌─────────────────────────────────────────────────────────────────┐
│  WHY SUBAGENTS FOR TRAVEL PLANNER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. USER EXPERIENCE                                             │
│     User wants to talk to a "travel advisor" - not be           │
│     transferred between departments or interact with            │
│     a faceless search system.                                   │
│                                                                 │
│  2. ORCHESTRATION COMPLEXITY                                    │
│     Planning requires judgment: "Should I search for            │
│     activities before or after confirming the hotel?"           │
│     Supervisor reasoning handles this dynamically.              │
│                                                                 │
│  3. SYNTHESIS REQUIREMENT                                       │
│     Final output must be a cohesive travel plan, not            │
│     just concatenated search results. Supervisor excels         │
│     at weaving components together.                             │
│                                                                 │
│  4. CONVERSATION CONTINUITY                                     │
│     "What about adding a day trip?" requires memory of          │
│     the existing plan. Supervisor maintains this state.         │
│                                                                 │
│  5. SPECIALIST FOCUS                                            │
│     Each domain (flights, hotels, activities) benefits          │
│     from focused prompts and tools, not a jack-of-all-trades.   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ System Architecture

```
                              User
                                │
                                ▼
                   ┌────────────────────────┐
                   │    SUPERVISOR AGENT    │
                   │    (Travel Advisor)    │
                   │                        │
                   │  • Understands request │
                   │  • Coordinates search  │
                   │  • Synthesizes plan    │
                   │  • Handles follow-ups  │
                   └───────────┬────────────┘
                               │
         ┌─────────────────────┼─────────────────────┬─────────────────────┐
         │                     │                     │                     │
         ▼                     ▼                     ▼                     ▼
   ┌───────────┐        ┌───────────┐        ┌────────────┐        ┌────────────┐
   │  FLIGHTS  │        │  HOTELS   │        │ ACTIVITIES │        │ ITINERARY  │
   │   AGENT   │        │   AGENT   │        │   AGENT    │        │   AGENT    │
   └─────┬─────┘        └─────┬─────┘        └─────┬──────┘        └─────┬──────┘
         │                     │                     │                     │
         ▼                     ▼                     ▼                     ▼
   ┌───────────┐        ┌───────────┐        ┌────────────┐        ┌────────────┐
   │• search   │        │• search   │        │• search    │        │• create    │
   │  flights  │        │  hotels   │        │  activities│        │  schedule  │
   │• compare  │        │• get      │        │• search    │        │• optimize  │
   │  prices   │        │  recommend│        │  restaurants        │  route     │
   └───────────┘        └───────────┘        │• get       │        │• generate  │
                                             │  recommend │        │  summary   │
                                             └────────────┘        └────────────┘
```

---

## 🤖 Agent Specifications

### 1. Supervisor Agent (Travel Advisor)

| Aspect                     | Details                                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------------- |
| **Role**             | Central coordinator - the "Travel Advisor"                                                     |
| **Persona**          | Professional, friendly travel advisor                                                          |
| **Responsibilities** | Parse user requirements, decide which subagents to call, synthesize results, handle follow-ups |
| **State**            | Maintains conversation history via checkpointer                                                |

**Tools (Wrapped Subagents):**

* `search_flights` - Invoke flights agent
* `search_hotels` - Invoke hotels agent
* `search_activities` - Invoke activities agent
* `create_itinerary` - Invoke itinerary agent

**System Prompt Focus:**

```
You are a professional travel planning assistant. Coordinate specialists
to create comprehensive travel plans. Be conversational, make specific
recommendations, and consider budget and preferences throughout.
```

---

### 2. Flights Agent

| Aspect              | Details                                           |
| ------------------- | ------------------------------------------------- |
| **Role**      | Flight Search Specialist                          |
| **Domain**    | Air travel search and recommendations             |
| **Expertise** | Routes, airlines, pricing, layovers, travel times |
| **State**     | Stateless (fresh context each call)               |

**Tools:**

| Tool                      | Purpose                  | Parameters                                         |
| ------------------------- | ------------------------ | -------------------------------------------------- |
| `search_flights`        | Find available flights   | `destination`,`budget_max`,`preferred_stops` |
| `compare_flight_prices` | Price comparison summary | `destination`                                    |

**System Prompt Focus:**

```
You are a flight search specialist. Find the best flights considering
budget, duration, and convenience. Highlight trade-offs between
cheapest, fastest, and most comfortable options.
```

---

### 3. Hotels Agent

| Aspect              | Details                                          |
| ------------------- | ------------------------------------------------ |
| **Role**      | Accommodation Specialist                         |
| **Domain**    | Accommodation search and recommendations         |
| **Expertise** | Hotels, neighborhoods, amenities, traveler types |
| **State**     | Stateless (fresh context each call)              |

**Tools:**

| Tool                         | Purpose               | Parameters                                             |
| ---------------------------- | --------------------- | ------------------------------------------------------ |
| `search_hotels`            | Find available hotels | `destination`,`budget_per_night`,`traveler_type` |
| `get_hotel_recommendation` | Personalized top pick | `destination`,`traveler_type`,`priority`         |

**System Prompt Focus:**

```
You are a hotel specialist. Match accommodations to traveler profiles.
Consider families need space and kid-friendly amenities, couples want
romantic settings, budget travelers need value. Location matters.
```

---

### 4. Activities Agent

| Aspect              | Details                                                   |
| ------------------- | --------------------------------------------------------- |
| **Role**      | Experiences Specialist                                    |
| **Domain**    | Things to do, attractions, restaurants                    |
| **Expertise** | Local experiences, cuisine, cultural sites, entertainment |
| **State**     | Stateless (fresh context each call)                       |

**Tools:**

| Tool                             | Purpose                     | Parameters                                   |
| -------------------------------- | --------------------------- | -------------------------------------------- |
| `search_activities`            | Find activities             | `destination`,`interests`,`budget_max` |
| `search_restaurants`           | Find dining options         | `destination`,`cuisine`,`price_range`  |
| `get_activity_recommendations` | Curated list for trip style | `destination`,`trip_style`,`num_days`  |

**System Prompt Focus:**

```
You are a local experiences specialist. Help travelers discover amazing
things to do. Mix popular attractions with hidden gems. Consider
interests, energy levels, and logistics. Recommend restaurants that
match the trip style.
```

---

### 5. Itinerary Agent

| Aspect              | Details                                             |
| ------------------- | --------------------------------------------------- |
| **Role**      | Schedule Optimizer                                  |
| **Domain**    | Schedule optimization and trip organization         |
| **Expertise** | Day planning, route optimization, pacing, logistics |
| **State**     | Stateless (fresh context each call)                 |

**Tools:**

| Tool                      | Purpose                          | Parameters                                                                      |
| ------------------------- | -------------------------------- | ------------------------------------------------------------------------------- |
| `create_daily_schedule` | Organize activities by day       | `activities`,`hotel_location`,`trip_pace`                                 |
| `optimize_route`        | Suggest efficient visiting order | `locations`                                                                   |
| `generate_trip_summary` | Complete trip document           | `destination`,`num_days`,`flight_info`,`hotel_info`,`activities_info` |

**System Prompt Focus:**

```
You are an itinerary planning expert. Organize travel components into
enjoyable, logical schedules. Consider geography (don't zigzag),
energy levels (intense activities early), and pacing (quality over
quantity). Build in rest time and meals.
```

---

## 🔗 Subagent Wrapping Strategy

Each subagent is wrapped as a tool for the supervisor using the `@tool` decorator:

```python
@tool
def search_flights(request: str) -> str:
    """Search for flights to a destination.
  
    Pass full context: destination, dates, budget, preferences.
    Example: "Find flights to Tokyo, budget $800, prefer direct"
    """
    result = flights_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].text
```

### Design Decisions

| Decision             | Choice                   | Rationale                                  |
| -------------------- | ------------------------ | ------------------------------------------ |
| **Input**      | Natural language request | Supervisor can provide rich context        |
| **Output**     | Final text only          | Supervisor doesn't need internal reasoning |
| **State**      | Stateless subagents      | Fresh context prevents cross-contamination |
| **Invocation** | Synchronous              | Supervisor needs results to continue       |

---

## 📁 Project Structure

```
travel_planner/
├── main.py                 # Entry point, demo scenarios
├── supervisor.py           # Supervisor agent + subagent wrappers
├── subagents/
│   ├── __init__.py
│   ├── flights.py          # Flights agent + tools
│   ├── hotels.py           # Hotels agent + tools
│   ├── activities.py       # Activities agent + tools
│   └── itinerary.py        # Itinerary agent + tools
├── tools/
│   ├── __init__.py
│   └── mock_data.py        # Mock travel data
├── requirements.txt
└── README.md
```

---

## 📅 Implementation Phases

| Phase             | Focus        | Deliverables                                                                                |
| ----------------- | ------------ | ------------------------------------------------------------------------------------------- |
| **Phase 1** | Data & Tools | Mock travel data (flights, hotels, activities, restaurants), tool functions for each domain |
| **Phase 2** | Subagents    | Four specialized agents with focused prompts - Flights, Hotels, Activities, Itinerary       |
| **Phase 3** | Wrapping     | Subagents wrapped as tools for supervisor using @tool decorator pattern                     |
| **Phase 4** | Supervisor   | Main orchestrating agent with all subagent tools and conversation memory                    |
| **Phase 5** | Integration  | End-to-end testing, demo scenarios, documentation                                           |

---

## 🔄 Expected Interaction Flow

### User Request

> *"Plan a 5-day trip to Tokyo for me and my wife. We love food and culture. Mid-range budget, around $3000 total."*

### Supervisor Processing

```
1. Parse Requirements
   ├── Destination: Tokyo
   ├── Duration: 5 days
   ├── Travelers: Couple
   ├── Interests: Food, Culture
   └── Budget: $3000 total

2. Call Flights Agent
   └── "Find flights to Tokyo, budget around $800-900 per person"
   
3. Call Hotels Agent
   └── "Find couple-friendly hotels in Tokyo, mid-range $150-200/night"
   
4. Call Activities Agent
   └── "Find food and cultural activities in Tokyo for a couple, 5 days"
   
5. Call Itinerary Agent
   └── "Create 5-day Tokyo itinerary with [flight], [hotel], [activities]"
   
6. Synthesize Final Response
   └── Cohesive travel plan with specific recommendations
```

### Output

Complete trip plan including:

* ✈️ Specific flight recommendation
* 🏨 Hotel recommendation with reasoning
* 🎯 Day-by-day activities and restaurants
* 📅 Organized itinerary with timing
* 💰 Budget breakdown
* 💡 Practical travel tips

---

## 💾 Data Layer

For this demo, we use mock data simulating real travel APIs:

| Data Type   | Mock Implementation      | Production Replacement                  |
| ----------- | ------------------------ | --------------------------------------- |
| Flights     | `MOCK_FLIGHTS`dict     | Amadeus, Skyscanner, Google Flights API |
| Hotels      | `MOCK_HOTELS`dict      | Booking.com, Hotels.com API             |
| Activities  | `MOCK_ACTIVITIES`dict  | TripAdvisor, Viator, GetYourGuide API   |
| Restaurants | `MOCK_RESTAURANTS`dict | Yelp, Google Places API                 |

---

## 💡 Key Takeaways

### 🎯 Centralized Control

Supervisor makes all routing decisions and maintains conversation state for natural follow-ups.

### 🔒 Context Isolation

Each subagent works in fresh context, preventing cross-domain pollution and improving focus.

### 🔄 Natural Synthesis

Supervisor weaves all results into cohesive recommendations, not just concatenated data.

### 💬 Conversation Continuity

Checkpointer enables multi-turn conversations: *"What about adding a day trip to Mt. Fuji?"*

---

## 📊 Summary Table

| Component                  | Type         | Tools               | State                   |
| -------------------------- | ------------ | ------------------- | ----------------------- |
| **Supervisor**       | Orchestrator | 4 wrapped subagents | Stateful (checkpointer) |
| **Flights Agent**    | Specialist   | 2 tools             | Stateless               |
| **Hotels Agent**     | Specialist   | 2 tools             | Stateless               |
| **Activities Agent** | Specialist   | 3 tools             | Stateless               |
| **Itinerary Agent**  | Specialist   | 3 tools             | Stateless               |

---

*Smart Travel Planner • SubAgents Pattern Demo • LangChain/LangGraph*
