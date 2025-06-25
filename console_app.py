import os
import sys
import time
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update, delete
import asyncio
from app.models.agent import Agent
from config import settings

DB_URL = settings.DATABASE_URL
engine = create_async_engine(DB_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
def pause():
    input("\nPress Enter to continue...")

# Testing db connection
async def test_db_connection():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda c: None)
        return True
    except Exception as e:
        print(f"Database connection test: Failed ({e})")
        return False
      
# View all agents
async def view_all_agents():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Agent))
        agents = result.scalars().all()
        print("\n === ALL AGENTS ===")
        if not agents:
            print("No agents found.")
        for agent in agents:
            print(f"  ID: {agent.id} | Agent [{agent.codename}] - {agent.realname} | Location: {agent.location} | Status: {agent.status.capitalize()} | Missions: {agent.missionscompleted}")
    pause()            
    
# Add new agent
async def add_new_agent():
    print("\n=== ADD NEW AGENT ===")
    codename = input("Codename: ").strip()
    realname = input("Real Name: ").strip()
    location = input("Location: ").strip()
    status = input("Status (active/inactive/on_mission/retired/deceased): ").strip().lower()
    missions = input("Missions Completed [0]: ").strip()
    missions = int(missions) if missions.isdigit() else 0
    async with AsyncSessionLocal() as session:
        agent = Agent(codename=codename, realname=realname, location=location, status=status, missionscompleted=missions)
        session.add(agent)
        try:
            await session.commit()
            print("Agent added successfully!")
        except Exception as e:
            await session.rollback()
            print(f"Error: {e}")
    pause()
    
# Update agent location
async def update_agent_location():
    print("\n=== UPDATE AGENT LOCATION ===")
    agent_id = input("Agent ID: ").strip()
    new_location = input("New Location: ").strip()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Agent).where(Agent.id == agent_id))
        agent = result.scalar_one_or_none()
        if not agent:
            print("Agent not found.")
        else:
            agent.location = new_location
            await session.commit()
            print("Location updated!")
    pause()

# Delete an agent
async def delete_agent():
    print("\n=== DELETE AGENT ===")
    agent_id = input("Agent ID: ").strip()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Agent).where(Agent.id == agent_id))
        agent = result.scalar_one_or_none()
        if not agent:
            print("Agent not found.")
        else:
            await session.delete(agent)
            await session.commit()
            print("Agent deleted.")
    pause()
    
# Search agent
async def search_agents():
    print("\n=== SEARCH AGENTS ===")
    term = input("Search by codename or real name: ").strip()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Agent).where((Agent.codename.ilike(f"%{term}%")) | (Agent.realname.ilike(f"%{term}%"))))
        agents = result.scalars().all()
        if not agents:
            print("No agents found.")
        else:
            for agent in agents:
                print(f"  ID: {agent.id} | Agent [{agent.codename}] - {agent.realname} | Location: {agent.location} | Status: {agent.status.capitalize()} | Missions: {agent.missionscompleted}")
    pause()
    
# Getting status report
async def status_report():
    print("\n=== STATUS REPORT ===")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Agent.status, Agent.id))
        statuses = {}
        for status, _ in result:
            statuses[status] = statuses.get(status, 0) + 1
        for status, count in statuses.items():
            print(f"{status.capitalize()}: {count} agent(s)")
    pause()
    
# Mission Count Addition
async def add_mission_count():
    print("\n=== ADD MISSION COUNT ===")
    agent_id = input("Agent ID: ").strip()
    count = input("How many missions to add? [1]: ").strip()
    count = int(count) if count.isdigit() else 1
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Agent).where(Agent.id == agent_id))
        agent = result.scalar_one_or_none()
        if not agent:
            print("Agent not found.")
        else:
            agent.missionscompleted += count
            await session.commit()
            print(f"Added {count} mission(s) to agent {agent.codename}.")
    pause()
    
# Main Function
async def main_menu():
    clear()
    print("=== EAGLE EYE FIELD AGENT MANAGEMENT SYSTEM ===\n")
    print("Database connection test:", end=" ")
    if await test_db_connection():
        print("Success")
        print("Database connection established.\n")
    else:
        print("Failed\n")
        print("Exiting...")
        sys.exit(1)
    while True:
        print("=== MAIN MENU ===")
        print("1. View All Agents")
        print("2. Add New Agent")
        print("3. Update Agent Location")
        print("4. Delete Agent")
        print("5. Search Agents")
        print("6. Status Report")
        print("7. Add Mission Count")
        print("0. Exit\n")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            clear()
            await view_all_agents()
            clear()
        elif choice == "2":
            clear()
            await add_new_agent()
            clear()
        elif choice == "3":
            clear()
            await update_agent_location()
            clear()
        elif choice == "4":
            clear()
            await delete_agent()
            clear()
        elif choice == "5":
            clear()
            await search_agents()
            clear()
        elif choice == "6":
            clear()
            await status_report()
            clear()
        elif choice == "7":
            clear()
            await add_mission_count()
            clear()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)
            clear()

if __name__ == "__main__":
    asyncio.run(main_menu()) 