"""Agent model representing the agents table."""

class Agent:
    """
    Agent model representing the agents table.
    """
    def __init__(self, id, codename, realname, location, status, missionscompleted):
        self.id = id
        self.codename = codename
        self.realname = realname
        self.location = location
        self.status = status
        self.missionscompleted = missionscompleted

    def __str__(self):
        """
        Return a string representation of the agent.
        """
        return (
            f"ID: {self.id} | Codename: {self.codename} | Name: {self.realname} | "
            f"Location: {self.location} | Status: {self.status} | Missions: {self.missionscompleted}"
        )

    def to_dict(self):
        """Convert agents to dictionary representation"""
        return {
            "id": self.id,
            "codename": self.codename,
            "realname": self.realname,
            "location": self.location,
            "status": self.status,
            "missionscompleted": self.missionscompleted
        }
    