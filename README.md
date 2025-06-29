# Website Manager - Full Stack Flask & PostgreSQL Application

This is a full-stack, containerized web application that allows users to sign up, log in, and manage a personal list of websites. The application is built with Flask for the backend, PostgreSQL for the database, and is orchestrated entirely with Docker Compose for easy setup and deployment.

## Features

-   **Full User Authentication**: Secure signup, login, and logout functionality.
-   **Session Management**: User sessions are maintained to keep users logged in.
-   **CRUD Functionality**: Users can add (Create), view (Read), and delete their own websites.
-   **Persistent PostgreSQL Database**: All user and website data is stored in a PostgreSQL database that persists across container restarts thanks to Docker volumes.
-   **Multi-Container Architecture**: Uses Docker Compose to manage the Flask web application and the PostgreSQL database as separate, linked services.
-   **Automated Database Initialization**: On first run, the database is automatically set up with the required schema and seeded with sample data.
-   **Clean, Modern UI**: A responsive user interface built with Tailwind CSS.

## Technology Stack

-   **Backend**: Python, Flask, Werkzeug
-   **Database**: PostgreSQL
-   **Database Driver**: `psycopg2-binary`
-   **Frontend**: HTML, Tailwind CSS (via CDN)
-   **Containerization**: Docker, Docker Compose
-   **Environment Management**: `python-dotenv`

---

### 1. Configuration

The application and database are configured using a single `.env` file.

1.  Clone the repository:
    ```bash
    git clone https://github.com/AnantSom/Website-Manager.git
    cd website-manager
    ```

2.  Create a file named `.env` in the root of the project directory.

3.  Copy and paste the following content into your `.env` file. You can keep these default values or change them as needed.

    ```ini
    POSTGRES_DB=website_db
    POSTGRES_USER=flask_user
    POSTGRES_PASSWORD=mysecretpassword
    DB_NAME=website_db
    DB_USER=flask_user
    DB_PASSWORD=mysecretpassword
    DB_HOST=localhost
    DB_PORT=5433
    PUBLIC_PORT=10001
    FLASK_RUN_PORT=10000
    ```
### 2. Running the Application

You can run the full application stack using a single command.

#### Method A: Using Docker & Docker Compose (Recommended)

1.  Make sure Docker Desktop is running.
2.  From the project's root directory, run the following command:
    ```bash
    docker-compose up --build
    ```
    *   This will build the Flask application image, pull the PostgreSQL image, create a persistent volume for the database, and start both containers.
    *   The first time you run this, the `initdb` scripts will create the tables and add sample users.
3.  The web application will be available at **http://localhost:10001** (or your `PUBLIC_PORT`).

4.  **You can log in with the sample user accounts from the seed data:**
    *   **Username:** `anant` / **Password:** `1234`
    *   **Username:** `aditya` / **Password:** `4567`

5.  To stop the application, press `CTRL+C`. To stop and remove the containers, run:
    ```bash
    docker-compose down
    ```
#### Method B: Running Locally (Hybrid Approach)

If you wish to run the Flask application locally for easier debugging but still use the containerized database:

1.  **Set up a local Python environment:**
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt
    ```

2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will connect to the Dockerized database and will be available at **http://localhost:10000** (or your `FLASK_RUN_PORT`).
---
