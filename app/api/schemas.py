"""Schema for API request/response validation"""

from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional
from enum import Enum

class AgentStatus(str, Enum):
    """Enum for agent status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_MISSION = "on_mission"
    RETIRED = "retired"
    DECEASED = "deceased"
    
    
class AgentBase(BaseModel):
    """Base agent schema with common fields"""
    codename: str = Field(..., min_length=1, max_length=50, description="Agent's codename")
    realname: str = Field(..., min_length=1, max_length=100, description="Agent's real name")
    location: str = Field(..., min_length=1, max_length=100, description="Agent's current location")
    status: AgentStatus = Field(..., description="Agent's current status")
    
    @validator('codename')
    def validate_codename(cls, v):
        """Validate codename format"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Codename must contain only alphanumeric characters, underscores, and hyphens')
        return v
    
    
class AgentCreate(AgentBase):
    """Schema for creating a new agent"""
    missionscompleted: int = Field(default=0, ge=0, description="Number of missions completed")
    

class AgentUpdate(BaseModel):
    """Schema for updating an agent."""
    codename: Optional[str] = Field(None, min_length=1, max_length=50)
    realname: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[AgentStatus] = None
    missionscompleted: Optional[int] = Field(None, ge=0)


class AgentResponse(AgentBase):
    """Schema for agent response."""
    id: int
    missionscompleted: int
    
    model_config = ConfigDict(from_attributes=True)


class AgentListResponse(BaseModel):
    """Schema for list of agents response."""
    agents: list[AgentResponse]
    total: int
    page: int
    size: int


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    success: bool = True 
    