# Insurance Policy Manager

A Windows application for managing and tracking insurance policies for clients. This application allows you to:
- Add new clients with their contact information
- Add insurance policies for clients
- Search for clients and view their policy details
- Track investments across different insurance companies

## Setup Instructions

1. Make sure you have Python 3.8 or higher installed on your system.

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python insurance_manager.py
```

## How to Use

1. **Adding a New Client**
   - Fill in the client's name (required), contact number, and email
   - Click "Add Client" to save the client information

2. **Adding a Policy**
   - First, add or search for a client
   - Fill in the policy details:
     - Policy Type (e.g., Life Insurance, Health Insurance)
     - Company Name
     - Policy Number
     - Investment Amount
   - Click "Add Policy" to save the policy information

3. **Searching for Clients**
   - Enter the client's name in the search box
   - Click "Search" to view all policies associated with the client
   - Results will show in the table below with complete details

## Features

- Modern and user-friendly interface
- SQLite database for persistent storage
- Search functionality for quick access to client information
- Detailed view of all policies and investments
- Error handling and input validation

## Data Storage

The application uses SQLite database (insurance.db) to store all client and policy information. The database is automatically created when you first run the application. 