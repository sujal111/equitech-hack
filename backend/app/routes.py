from fastapi import APIRouter
from .schemas import IncidentCreate, IncidentResponse
from .workflows import handle_incident

router = APIRouter()

@router.post("/incident", response_model=IncidentResponse)
async def create_incident(incident: IncidentCreate):
    result = await handle_incident(incident)
    return result
