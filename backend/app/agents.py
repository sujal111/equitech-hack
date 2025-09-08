from langgraph.graph import StateGraph
from pydantic import BaseModel


# Define the state schema for the LangGraph
class IncidentState(BaseModel):
    incident: dict
    status: str = "pending"


async def incident_agent(incident: dict):
    # Initialize graph with schema
    graph_builder = StateGraph(IncidentState)

    # Define a simple analysis node
    async def analyze(state: IncidentState):
        return IncidentState(
            incident=incident,
            status=f"Incident '{incident['title']}' acknowledged ✅"
        )

    # Register node and entrypoint
    graph_builder.add_node("analyze", analyze)
    graph_builder.set_entry_point("analyze")

    # Compile the graph
    app = graph_builder.compile()

    # Run the graph
    final_state = await app.ainvoke(IncidentState(incident=incident, status="pending"))

    return final_state.status
