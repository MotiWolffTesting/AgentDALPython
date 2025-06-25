"""Agent service with business logic and CRUD operations."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.models.agent import Agent
from app.api.schemas import AgentCreate, AgentUpdate, AgentStatus


class AgentService:
    """Service class for agent-related operations"""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        
    async def create_agent(self, agent_data: AgentCreate) -> Agent:
        """Create agent"""
        agent = Agent(
            codename=agent_data.codename,
            realname=agent_data.realname,
            location=agent_data.location,
            status=agent_data.status.value,
            missionscompleted=agent_data.missionscompleted
        )
        
        self.db.add(agent)
        await self.db.commit()
        await self.db.refresh(agent)
        return agent
    
    async def get_agent_by_id(self, agent_id: int) -> Optional[Agent]:
        """
        Get agent by ID.
        """
        result = await self.db.execute(
            select(Agent).where(Agent.id == agent_id)
        )
        return result.scalar_one_or_none()
    
    async def get_agent_by_codename(self, codename: str) -> Optional[Agent]:
        """
        Get agent by codename.
        """
        result = await self.db.execute(
            select(Agent).where(Agent.codename == codename)
        )
        return result.scalar_one_or_none()
    
    async def get_all_agents(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[AgentStatus] = None
    ) -> tuple[List[Agent], int]:
        """
        Get all agents with optional filtering and pagination.
        """
        query = select(Agent)
        
        if status:
            query = query.where(Agent.status == status.value)
        
        # Get total count
        count_query = select(Agent.id)
        if status:
            count_query = count_query.where(Agent.status == status.value)
        
        count_result = await self.db.execute(count_query)
        total = len(count_result.scalars().all())
        
        # Get paginated results
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        agents = result.scalars().all()
        
        return agents, total
    
    async def update_agent(self, agent_id: int, agent_data: AgentUpdate) -> Optional[Agent]:
        """
        Update an existing agent.
        """
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            return None
        
        update_data = agent_data.model_dump(exclude_unset=True)
        
        # Convert status enum to string if provided
        if 'status' in update_data:
            update_data['status'] = update_data['status'].value
        
        for field, value in update_data.items():
            setattr(agent, field, value)
        
        await self.db.commit()
        await self.db.refresh(agent)
        return agent
    
    async def delete_agent(self, agent_id: int) -> bool:
        """
        Delete an agent.
        """
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            return False
        
        await self.db.delete(agent)
        await self.db.commit()
        return True
    
    async def increment_missions(self, agent_id: int) -> Optional[Agent]:
        """
        Increment the missions completed count for an agent.
        """
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            return None
        
        agent.missionscompleted += 1
        await self.db.commit()
        await self.db.refresh(agent)
        return agent
    
    async def update_agent_status(self, agent_id: int, status: AgentStatus) -> Optional[Agent]:
        """
        Update agent status.
        """
        agent = await self.get_agent_by_id(agent_id)
        if not agent:
            return None
        
        agent.status = status.value
        await self.db.commit()
        await self.db.refresh(agent)
        return agent
    
    async def get_agents_by_status(self, status: AgentStatus) -> List[Agent]:
        """
        Get all agents with a specific status.
        """
        result = await self.db.execute(
            select(Agent).where(Agent.status == status.value)
        )
        return result.scalars().all()
    
    async def get_top_performers(self, limit: int = 10) -> List[Agent]:
        """
        Get top performing agents by missions completed.
        """
        result = await self.db.execute(
            select(Agent)
            .order_by(Agent.missionscompleted.desc())
            .limit(limit)
        )
        return result.scalars().all() 