from app.dal.agent_dal import AgentDAL
from app.models.agent import Agent
import sys
import time

# Clear the console
def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

# Pause the program
def pause():
    input("\nPress Enter to continue...")

# Initialize the database connection
dal = AgentDAL()

# Test the database connection
def test_db_connection():
    try:
        dal.get_all_agents()
        return True
    except Exception as e:
        print(f"Database connection test: Failed ({e})")
        return False
    
# View all agents
def view_all_agents():
    agents = dal.get_all_agents()
    print("\n === ALL AGENTS ===")
    if not agents:
        print("No agents found.")
    for agent in agents:
        print(agent)
    pause()

# Add a new agent
def add_new_agent():
    print("\n=== ADD NEW AGENT ===")
    codename = input("Codename: ").strip()
    realname = input("Real Name: ").strip()
    location = input("Location: ").strip()
    status = input("Status (Active/Injured/Missing/Retired): ").strip().capitalize()
    missions = input("Missions Completed [0]: ").strip()
    missions = int(missions) if missions.isdigit() else 0
    try:
        dal.add_agent(codename, realname, location, status, missions)
        print("Agent added successfully!")
    except Exception as e:
        print(f"Error: {e}")
    pause()

# Update an agent's location
def update_agent_location():
    print("\n=== UPDATE AGENT LOCATION ===")
    agent_id = input("Agent ID: ").strip()
    new_location = input("New Location: ").strip()
    dal.update_agent_location(agent_id, new_location)
    print("Location updated!")
    pause()

# Delete an agent
def delete_agent():
    print("\n=== DELETE AGENT ===")
    agent_id = input("Agent ID: ").strip()
    dal.delete_agent(agent_id)
    print("Agent deleted.")
    pause()

# Search for agents
def search_agents():
    print("\n=== SEARCH AGENTS ===")
    term = input("Search by codename or real name: ").strip()
    agents = dal.search_agents(term)
    if not agents:
        print("No agents found.")
    else:
        for agent in agents:
            print(agent)
    pause()

# Generate a status report
def status_report():
    print("\n=== STATUS REPORT ===")
    report = dal.status_report()
    for status, count in report:
        print(f"{status}: {count} agent(s)")
    pause()

# Add mission count
def add_mission_count():
    print("\n=== ADD MISSION COUNT ===")
    agent_id = input("Agent ID: ").strip()
    count = input("How many missions to add? [1]: ").strip()
    count = int(count) if count.isdigit() else 1
    dal.add_mission_count(agent_id, count)
    print(f"Added {count} mission(s) to agent.")
    pause()

# Main menu
def main_menu():
    clear()
    print("=== EAGLE EYE FIELD AGENT MANAGEMENT SYSTEM ===\n")
    print("Database connection test:", end=" ")
    if test_db_connection():
        print("Success")
        print("Database connection established.\n")
    else:
        print("Failed\n")
        print("Exiting...")
        sys.exit(1)
    # Main menu loop
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
            view_all_agents()
            clear()
        elif choice == "2":
            clear()
            add_new_agent()
            clear()
        elif choice == "3":
            clear()
            update_agent_location()
            clear()
        elif choice == "4":
            clear()
            delete_agent()
            clear()
        elif choice == "5":
            clear()
            search_agents()
            clear()
        elif choice == "6":
            clear()
            status_report()
            clear()
        elif choice == "7":
            clear()
            add_mission_count()
            clear()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
            time.sleep(1)
            clear()

if __name__ == "__main__":
    main_menu() 