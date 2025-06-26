import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from app.dal.agent_dal import AgentDAL

class AgentManagerGUI:
    """ 
    TKInter Class for managing the GUI
    """
    def __init__(self, root):
        self.root = root # Root window
        self.root.title('Eagle Eye Agent Manager') # Set the title of the window
        self.dal = AgentDAL() # Initialize the database connection
        self.create_widgets() # Create the widgets
        self.refresh_agents() # Refresh the agents

    def create_widgets(self):
        """
        Create the widgets for the GUI.
        """
        # Search bar
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT) # Using pack instead of grid to place the label in the search frame
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT)
        tk.Button(search_frame, text="Search", command=self.search_agents).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Show All", command=self.refresh_agents).pack(side=tk.LEFT)

        # Agent list
        self.tree = ttk.Treeview(self.root, columns=("ID", "Codename", "Name", "Location", "Status", "Missions"), show="headings", selectmode="browse")
        for col in ("ID", "Codename", "Name", "Location", "Status", "Missions"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Action buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Delete Agent", command=self.delete_agent).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Update Location", command=self.update_location).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Increment Missions", command=self.increment_missions).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Status Report", command=self.status_report).pack(side=tk.LEFT, padx=5)

        # Add agent form
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Codename:").grid(row=0, column=0)
        tk.Label(form_frame, text="Name:").grid(row=0, column=2)
        tk.Label(form_frame, text="Location:").grid(row=1, column=0)
        tk.Label(form_frame, text="Status:").grid(row=1, column=2)
        tk.Label(form_frame, text="Missions:").grid(row=2, column=0)

        self.codename_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.missions_var = tk.StringVar(value="0")

        tk.Entry(form_frame, textvariable=self.codename_var).grid(row=0, column=1)
        tk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=3)
        tk.Entry(form_frame, textvariable=self.location_var).grid(row=1, column=1)
        tk.Entry(form_frame, textvariable=self.status_var).grid(row=1, column=3)
        tk.Entry(form_frame, textvariable=self.missions_var).grid(row=2, column=1)

        tk.Button(form_frame, text="Add Agent", command=self.add_agent).grid(row=2, column=3, padx=10)

    # Function to refresh the agents
    def refresh_agents(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            agents = self.dal.get_all_agents()
            for agent in agents:
                self.tree.insert("", tk.END, values=(agent.id, agent.codename, agent.realname, agent.location, agent.status, agent.missionscompleted))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load agents: {e}")

    # Function to search for agents
    def search_agents(self):
        term = self.search_var.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            agents = self.dal.search_agents(term)
            for agent in agents:
                self.tree.insert("", tk.END, values=(agent.id, agent.codename, agent.realname, agent.location, agent.status, agent.missionscompleted))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search agents: {e}")

    # Function to add an agent
    def add_agent(self):
        codename = self.codename_var.get().strip()
        name = self.name_var.get().strip()
        location = self.location_var.get().strip()
        status = self.status_var.get().strip()
        missions = self.missions_var.get().strip()
        if not codename or not name or not location or not status:
            messagebox.showwarning("Input Error", "All fields except Missions are required.")
            return
        try:
            missions = int(missions) if missions.isdigit() else 0
            self.dal.add_agent(codename, name, location, status, missions)
            messagebox.showinfo("Success", "Agent added successfully!")
            self.codename_var.set("")
            self.name_var.set("")
            self.location_var.set("")
            self.status_var.set("")
            self.missions_var.set("0")
            self.refresh_agents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add agent: {e}")

    # Function to get the selected agent id
    def get_selected_agent_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "No agent selected.")
            return None
        return self.tree.item(selected[0])["values"][0]

    # Function to delete an agent
    def delete_agent(self):
        agent_id = self.get_selected_agent_id()
        if agent_id is None:
            return
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this agent?"):
            return
        try:
            self.dal.delete_agent(agent_id)
            messagebox.showinfo("Success", "Agent deleted.")
            self.refresh_agents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete agent: {e}")

    # Function to update the location of an agent
    def update_location(self):
        agent_id = self.get_selected_agent_id()
        if agent_id is None:
            return
        new_location = simpledialog.askstring("Update Location", "Enter new location:")
        if not new_location:
            return
        try:
            self.dal.update_agent_location(agent_id, new_location)
            messagebox.showinfo("Success", "Location updated!")
            self.refresh_agents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update location: {e}")

    # Function to increment the missions of an agent
    def increment_missions(self):
        agent_id = self.get_selected_agent_id()
        if agent_id is None:
            return
        try:
            self.dal.add_mission_count(agent_id, 1)
            messagebox.showinfo("Success", "Missions incremented by 1.")
            self.refresh_agents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to increment missions: {e}")

    # Function to get the status report
    def status_report(self):
        try:
            report = self.dal.status_report()
            msg = "Status Report:\n" + "\n".join(f"{status}: {count} agent(s)" for status, count in report)
            messagebox.showinfo("Status Report", msg)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get status report: {e}")

# Main function to run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = AgentManagerGUI(root)
    root.mainloop()
