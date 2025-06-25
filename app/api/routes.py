"""FastAPI routes"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from typing import Optional
from app.database.connection import get_db_session
from app.services.agent_service import AgentService
from app.api.schemas import (
    AgentCreate, AgentUpdate, AgentResponse, AgentListResponse, 
    MessageResponse, AgentStatus
)

# Define the router for the agents API
router = APIRouter(prefix="/api/v1/agents", tags=["agents"])


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    db: AsyncSession = Depends[get_db_session]
):
    """Create a new agent"""
    service = AgentService(db)
    
    # Check if codename already exists
    existing_agent = await service.get_agent_by_codename(agent_data.codename)
    if existing_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Agent with codename {agent_data.codename} already exists."
        )
        
    agent = await service.create_agent(agent_data)
    return agent


router.get("/", response_model=AgentListResponse)
async def get_agents(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    status: Optional[AgentStatus] = Query(None, description="Filter by agent status"),
    db: AsyncSession = Depends(get_db_session)
):
    """Get all agents with optional filtering"""
    service = AgentService(db)
    agents, total = await service.get_all_agents(skip=skip, limit=limit, status=status)
    
    return AgentListResponse(
        agents=agents,
        total=total,
        page=skip // limit + 1,
        size=len(agents)
    )
    
    
router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    db: AsyncSession = Depends[get_db_session]
):
    """Get agent by ID"""
    service = AgentService(db)
    agent = await service.get_agent_by_id(agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found."
        )
        
    return agent


router.get("/codename/{codename}", response_model=AgentResponse)
async def get_agent_by_codename(
    codename: str,
    db: AsyncSession = Depends[get_db_session]
):
    """Get agent by codename"""
    service = AgentService(db)
    agent = service.get_agent_by_codename(codename)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with codename {codename} not found."
        )
        
    return agent


router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    db: AsyncSession = Depends[get_db_session]
):
    """Update an existing agent"""
    service = AgentService(db)
    
    # Check if agent exists
    existing_agent = service.get_agent_by_id(agent_id)
    if not existing_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found."
        )
        
    # Check if codename is being updated and if it already exists
    if agent_data.codename and agent_data.codename != existing_agent.codename:
        codename_exists = await service.get_agent_by_codename(agent_data.codename)
        if codename_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Agent with codename {agent_data.codename} already exists."
            )
            
    agent = await service.update_agent(agent_id, agent_data)
    return agent


router.delete("/{agent_id}", response_model=AgentResponse)
async def delete_agent(
    agent_id: int,
    db: AsyncSession = Depends[get_db_session]
):
    """Delete agent by ID"""
    service = AgentService(db)
    success = await service.delete_agent(agent_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found."
        )
        
    return MessageResponse(message=f"Agent with id {agent_id} successfully deleted.")


router.patch("/{agent_id}/increment-mission", response_model=AgentResponse)
async def increment_missions(
    agent_id: int,
    db: AsyncSession = Depends[get_db_session]
):
    """Increment the missions completed count for an agent"""
    service = AgentService(db)
    agent = await service.increment_missions(agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found."
        )
        
    return agent


router.patch("/{agent_id}/status", response_model=AgentResponse)
async def update_agent_status(
    agent_id: int,
    status: AgentStatus,
    db: AsyncSession = Depends[get_db_session]
):
    """Update agent status"""
    service = AgentService(db)
    agent = service.update_agent_status(agent_id, status)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with id {agent_id} not found."
        )
        
    return agent


@router.get("/status/{status}", response_model=list[AgentResponse])
async def get_agents_by_status(
    status: AgentStatus,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get all agents with a specific status.
    """
    service = AgentService(db)
    agents = await service.get_agents_by_status(status)
    return agents


@router.get("/top-performers/", response_model=list[AgentResponse])
async def get_top_performers(
    limit: int = Query(10, ge=1, le=100, description="Number of top performers to return"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get top performing agents by missions completed.
    """
    service = AgentService(db)
    agents = await service.get_top_performers(limit=limit)
    return agents 
    
    