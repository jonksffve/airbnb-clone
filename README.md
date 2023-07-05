# Airbnb clone - Learning project.

This is a project used for learning purposes. Goal was to build an airbnb-like structure to practice Django, Django Rest Framework and React to understand better these technologies in a practical way.

## Project structure

Project follows a typical Django project structure with the frontend built using React. Main technologies and components:

backend: Directory that contains the **Django** project setup, configuration files, including the settings, URL routing, database models and **Django Rest Framework**, support files such as views and endpoint urls.

frontend: This directory contains the **React** application code, including the components, styles **(made with Tailwind css)**, and assets. Frontend was built with the help of Vite, React router, React redux among other useful tools.

## Installation
To run this project locally, follow these steps:

## Backend Setup
- Clone the repository.
- Navigate to the backend directory: cd backend
- Create a virtual environment: python -m venv venv
- Activate the virtual environment:
- For Windows: venv\Scripts\activate
- For Unix or Linux: source venv/bin/activate
- Install the required Python packages: pip install -r requirements.txt
- Apply database migrations: python manage.py migrate
- Start the backend server: python manage.py runserver

## Frontend Setup
- Open a new terminal window/tab.
- Navigate to the frontend directory: cd frontend
- Install the required Node packages: npm install
- Start the frontend development server: npm run dev
