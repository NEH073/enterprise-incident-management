from enum import Enum

from pydantic import BaseModel


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Status(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class IncidentCreate(BaseModel):
    title: str
    description: str
    priority: Priority
    status: Status = Status.OPEN
    assigned_to: int | None = None


class IncidentUpdate(BaseModel):
    title: str
    description: str
    priority: Priority
    status: Status
    assigned_to: int | None = None

class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: Priority
    status: str
    assigned_to: int | None = None
    assigned_username: str | None = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class IncidentAssign(BaseModel):
    assigned_to: int | None = None