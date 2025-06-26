import os
from dotenv import load_dotenv
import mysql.connector
from app.models.agent import Agent

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

class AgentDAL:
    """
    Data Access Layer for the agents table.
    """
    def __init__(self):
        self.db_config = DB_CONFIG

    def get_connection(self):
        """
        Get a connection to the database.
        """
        return mysql.connector.connect(**self.db_config)

    def get_all_agents(self):
        """
        Get all agents from the database.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, codeName, realName, location, status, missionsCompleted FROM agents")
        agents = [Agent(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return agents

    def add_agent(self, codename, realname, location, status, missions):
        """
        Add a new agent to the database.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO agents (codeName, realName, location, status, missionsCompleted) VALUES (%s, %s, %s, %s, %s)",
                (codename, realname, location, status, missions)
            )
            conn.commit()
            success = True
        except Exception as e:
            conn.rollback()
            success = False
            raise e
        finally:
            cursor.close()
            conn.close()
        return success

    def update_agent_location(self, agent_id, new_location):
        """
        Update an agent's location in the database.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE agents SET location=%s WHERE id=%s", (new_location, agent_id))
        conn.commit()
        cursor.close()
        conn.close()

    def delete_agent(self, agent_id):
        """
        Delete an agent from the database.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agents WHERE id=%s", (agent_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def search_agents(self, term):
        """
        Search for agents in the database.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, codeName, realName, location, status, missionsCompleted FROM agents WHERE codeName LIKE %s OR realName LIKE %s", (f"%{term}%", f"%{term}%"))
        agents = [Agent(*row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return agents

    def status_report(self):
        """
        Generate a status report of agents by status.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) FROM agents GROUP BY status")
        report = cursor.fetchall()
        cursor.close()
        conn.close()
        return report

    def add_mission_count(self, agent_id, count):
        """
        Add a mission count to an agent's missions completed.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE agents SET missionsCompleted = missionsCompleted + %s WHERE id=%s", (count, agent_id))
        conn.commit()
        cursor.close()
        conn.close() 