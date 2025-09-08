import uuid
from .agents import incident_agent
from .schemas import IncidentResponse


async def handle_incident(incident):
    ai_message = await incident_agent(incident)
    return IncidentResponse(
        id=str(uuid.uuid4()),
        status="In Progress",
        message=ai_message
    )
