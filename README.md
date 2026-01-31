# 🌏 Smart Travel Planner

A multi-agent travel planning system demonstrating the **SubAgents pattern** from LangChain/LangGraph.

## Overview

This project showcases how to build a multi-agent system where a central **Supervisor Agent** coordinates specialized **Subagents** to create comprehensive travel plans.

```

User Request

     │

     ▼

┌─────────────────┐

│   SUPERVISOR    │ ← Makes routing decisions

│     AGENT       │ ← Synthesizes results

└────────┬────────┘

         │

┌────────┴────────┬─────────────────┬─────────────────┐

▼                 ▼                 ▼                 ▼

┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐

│ FLIGHTS │  │ HOTELS  │  │ACTIVITIES│  │ITINERARY │

│  AGENT  │  │  AGENT  │  │  AGENT   │  │  AGENT   │

└─────────┘  └─────────┘  └──────────┘  └──────────┘

```

## Project Structure

```

travel_planner/

├── main.py              # Entry point with demo scenarios

├── supervisor.py        # Supervisor agent + subagent tool wrappers

├── subagents/

│   ├── __init__.py

│   ├── flights.py       # Flights search specialist

│   ├── hotels.py        # Hotels search specialist

│   ├── activities.py    # Activities & restaurants specialist

│   └── itinerary.py     # Itinerary planning specialist

├── tools/

│   ├── __init__.py

│   └── mock_data.py     # Mock travel data

└── requirements.txt

```

## Installation

1.**Clone and navigate to project:**

```bash

cd travel_planner

```

2.**Create virtual environment:**

```bash

python -m venv .venv

source .venv/bin/activate # On Windows: .venv\Scripts\activate

```

3.**Install dependencies:**

```bash

pip install -r requirements.txt

```

4.**Set your API key:**

```bash

export OPENAI_API_KEY='your-key-here'

# Or for Anthropic:

export ANTHROPIC_API_KEY='your-key-here'

```

## Usage

### Run Demo Scenarios

```bash

python main.py

```

This runs three demonstration scenarios:

1. Complete trip planning (all subagents)
2. Single domain request (hotels only)
3. Follow-up with conversation memory


## Implementation Details

### Supervisor Agent

The supervisor is created with `create_agent` and has four tools (wrapped subagents):

```python

supervisor = create_agent(

    model,

tools=[search_flights, search_hotels, search_activities, create_itinerary],

system_prompt=SUPERVISOR_PROMPT,

checkpointer=InMemorySaver(),  # For conversation memory

)

```

### Subagent Tool Wrapping

Each subagent is wrapped as a tool using the `@tool` decorator:

```python

@tool

def search_flights(request:str) ->str:

"""Search for flights to a destination."""

    result = flights_agent.invoke({

"messages": [{"role": "user", "content": request}]

    })

return result["messages"][-1].text  # Return only final text

```

### Key API Points

| Component        | API                                                       |

| ---------------- | --------------------------------------------------------- |

| Create agent     | `from langchain.agents import create_agent`             |

| Define tool      | `from langchain.tools import tool`                      |

| Initialize model | `from langchain.chat_models import init_chat_model`     |

| Memory           | `from langgraph.checkpoint.memory import InMemorySaver` |

## Extending the Project

### Add a New Subagent

1. Create `subagents/new_agent.py`:

```python

from langchain.agents import create_agent

from langchain.tools import tool


@tool

defnew_tool(query:str) ->str:

"""Tool description."""

return"result"


def create_new_agent(model):

return create_agent(

        model,

tools=[new_tool],

system_prompt="You are a specialist in...",

    )

```

2. Add wrapper in `supervisor.py`:

```python

@tool

def new_capability(request:str) ->str:

"""Description for supervisor."""

    result = new_agent.invoke(...)

return result["messages"][-1].text

```

3. Add to supervisor's tools list.

### Use Real APIs

Replace mock data functions in `tools/mock_data.py` with actual API calls:

- Flights: Amadeus, Skyscanner, Google Flights
- Hotels: Booking.com, Hotels.com
- Activities: TripAdvisor, Viator, GetYourGuide


## Further Reading

- [LangChain Multi-Agent Documentation](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [SubAgents Pattern Guide](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents)
- [Personal Assistant Tutorial](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant)

## License

MIT License - Feel free to use and modify for your own projects!
