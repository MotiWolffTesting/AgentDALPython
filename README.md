# Eagle Eye Agent Management System (CLI)

A simple Python CLI tool for managing field agent data using MySQL.

## Features

- **CRUD Operations**: Add, view, update, and delete agents
- **Search**: Find agents by codename or real name
- **Status Report**: See agent counts by status
- **Mission Tracking**: Increment missions completed
- **Environment-based DB config**: Secure credentials with `.env`

## Tech Stack

- **Python 3.8+**
- **Database**: MySQL
- **No ORM**: Direct SQL queries with `mysql-connector-python`

## Project Structure

```
AgentDAL/
├── app/
│   ├── models/
│   │   └── agent.py         # Agent class (plain Python)
│   ├── dal/
│   │   └── agent_dal.py    # Data Access Layer for MySQL
│   └── __init__.py
├── requirements.txt        # Python dependencies
├── console_app.py          # Main CLI application
├── README.md               # This file
└── .env                    # Environment variables (not committed)
```

## Database Schema

```sql
CREATE DATABASE IF NOT EXISTS eagleEyeDB;
USE eagleEyeDB;
CREATE TABLE IF NOT EXISTS agents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codeName VARCHAR(50) NOT NULL UNIQUE,
    realName VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    missionsCompleted INT NOT NULL DEFAULT 0
);
```

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AgentDAL
   ```
2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment**:
   Create a `.env` file in the root directory:
   ```env
   DB_HOST=localhost
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_NAME=eagleEyeDB
   ```
5. **Set up the MySQL database** (see schema above).

## Running the CLI Application

```bash
python console_app.py
```

## Example Menu
```
=== EAGLE EYE FIELD AGENT MANAGEMENT SYSTEM ===
1. View All Agents
2. Add New Agent
3. Update Agent Location
4. Delete Agent
5. Search Agents
6. Status Report
7. Add Mission Count
0. Exit
```

## Example Session
```
=== ADD NEW AGENT ===
Codename: 007
Real Name: James Bond
Location: London
Status (Active/Injured/Missing/Retired): Active
Missions Completed [0]: 100
Agent added successfully!

=== ALL AGENTS ===
ID: 1   | Codename: 007          | Name: James Bond          | Location: London        | Status: Active   | Missions: 100
```

## Development
- Follows PEP 8 guidelines. Use `black` for formatting:
  ```bash
  pip install black
  black .
  ```

## License
MIT License. 