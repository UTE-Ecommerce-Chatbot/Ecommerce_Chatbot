# Ecommerce Chatbot

This project is an Ecommerce Chatbot built using Rasa. Follow the instructions below to set up the environment, install the necessary libraries, and run the Rasa server along with custom actions.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Virtualenv (optional but recommended)

## Setup Instructions

### 1. Create a Virtual Environment (Optional but Recommended)

Creating a virtual environment helps to manage dependencies and avoid conflicts with other projects.

```bash
# Install virtualenv if you don't have it
pip install virtualenv

# Create a virtual environment named 'venv'
virtualenv venv

# Activate the virtual environment
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

### 2. Install Required Libraries 

- pip install -r requirements.txt

### 3. Train the Rasa Model

- rasa train

### 4. Run the Rasa Server

- rasa run --cors "*" --debug

### 5. Run Custom Actions

- rasa run actions --cors "*" --debug
