# Eagle Eye Agent Management System

A Python application for managing field agent data using MySQL, available as both CLI and GUI applications.

## Features

- **CRUD Operations**: Add, view, update, and delete agents
- **Search**: Find agents by codename or real name
- **Status Report**: See agent counts by status
- **Mission Tracking**: Increment missions completed
- **Multiple Interfaces**: CLI and GUI applications
- **Docker Support**: Easy deployment with Docker and MySQL
- **Environment-based DB config**: Secure credentials with environment variables



## Tech Stack

- **Python 3.11+**
- **Database**: MySQL 8.0
- **GUI**: Tkinter
- **No ORM**: Direct SQL queries with `mysql-connector-python`
- **Containerization**: Docker & Docker Compose

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
├── console_app.py          # CLI application
├── gui_app.py              # GUI application
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose orchestration
├── init.sql                # Database initialization script
├── env.example             # Environment variables template
├── .dockerignore           # Docker ignore file
└── README.md               # This file
```

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS agents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codeName VARCHAR(50) NOT NULL UNIQUE,
    realName VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    status ENUM('Active', 'Injured', 'Missing', 'Retired') DEFAULT 'Active',
    missionsCompleted INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

The database will be automatically created and populated with sample data when using Docker.

## Quick Start with Docker (Recommended)

The easiest way to run the application is using Docker Compose:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AgentDAL
   ```

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - The MySQL database will be available on port 3306
   - Sample data will be automatically loaded
   - To run the CLI application interactively:
     ```bash
     docker exec -it agent_dal_app python console_app.py
     ```
   - Or use the provided script:
     ```bash
     ./run_interactive.sh
     ```

4. **Stop the application**:
   ```bash
   docker-compose down
   ```

## Local Development Setup

If you prefer to run the application locally:

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
   Copy `env.example` to `.env` and update the values:
   ```bash
   cp env.example .env
   ```
   ```env
   DB_HOST=localhost
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_NAME=agentdb
   ```

5. **Set up MySQL database**:
   - Install MySQL 8.0
   - Create a database named `agentdb`
   - Run the SQL commands from `init.sql`

## Running the Applications

### CLI Application
```bash
python console_app.py
```

### GUI Application
```bash
python gui_app.py
```

**Note**: The GUI application requires a display server. When running in Docker, you'll need to set up X11 forwarding or use the CLI version.

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

## Docker Commands

### Build and run
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (will delete database data)
docker-compose down -v
```

### Individual container management
```bash
# Access the app container
docker exec -it agent_dal_app bash

# Run the console app interactively
docker exec -it agent_dal_app python console_app.py

# Access the MySQL container
docker exec -it agent_dal_mysql mysql -u agentuser -p agentdb

# View MySQL logs
docker logs agent_dal_mysql
```

## Development
- Follows PEP 8 guidelines. Use `black` for formatting:
  ```bash
  pip install black
  black .
  ```

## Troubleshooting

### Common Issues

1. **Port 3306 already in use**: 
   - Change the port mapping in `docker-compose.yml`
   - Or stop other MySQL instances

2. **Permission denied errors**:
   - Ensure Docker has proper permissions
   - Try running with `sudo` (Linux/macOS)

3. **Database connection fails**:
   - Wait for MySQL to fully start (healthcheck)
   - Check environment variables in `docker-compose.yml`

## License
MIT License. 