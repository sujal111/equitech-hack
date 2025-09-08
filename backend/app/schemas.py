from pydantic import BaseModel

class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str

class IncidentResponse(BaseModel):
    id: str
    status: str
    message: str
