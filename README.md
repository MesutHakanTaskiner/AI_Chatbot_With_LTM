# GPT

## Overview
Python-based project that implements a simple GPT-like application. It integrates AI operations, memory management, and a basic web interface, making it easy to experiment with natural language processing techniques.

Memory Management with mem0 (https://github.com/mem0ai/mem0)

This project uses mem0 to handle long-term memory in a smarter, more scalable way. mem0 enhances AI systems with intelligent memory, enabling them to remember user preferences, adapt over time, and deliver personalized experiences.

Key Benefits:

    Memory extraction and management
    Developer-friendly easy integration
    Scalable local memory

By leveraging mem0, the project benefits from a streamlined long-term memory system that aligns well with the expected behavior of GPT-like memory tools.

## Project Structure
- **Gemini Information**
Gemini is a state-of-the-art language model that serves as the primary in this project, processing natural language inputs and generating high-quality responses. Its integration is configured via the API key in the .env file, enabling robust dialogue management and advanced language understanding.

- **app.py**  
  The main entry point of the application. It initializes configurations, sets up modules, and orchestrates the workflow by importing necessary components from other modules.

- **requirements.txt**  
  Lists the Python dependencies required to run the project.

- **operations/**  
  Contains modules related to the core functionalities:
  - **ai.py**: Implements AI-related operations. This module likely includes functions that take an input string, process it through AI models or algorithms, and generate a response. It may involve pre-processing of input data, interaction with machine learning models, and post-processing of results.
  - **memory.py**: Manages the application’s state and conversation history. It likely defines functions or classes for storing, retrieving, and updating in-memory data to maintain continuity during interactions.

- **schemas/**  
  Defines data schemas and validations:
  - **schema.py**: Contains schema definitions for validating and transforming input and output data. It likely leverages libraries such as pydantic or similar to enforce data integrity and ensure that the data flowing through the application adheres to predefined rules.

- **templates/**  
  Stores HTML templates:
  - **index.html**: Serves as the primary template for the web interface. This file provides the structure for frontend display and may include placeholders for dynamic data insertion.

- **utils/**  
  General utilities for the project:
  - **__init__.py**: Marks the utils package. It may be used to expose common utility functions and configurations throughout the project.
  - **config.py**: Contains configuration settings and helper functions. This module likely reads environment variables or configuration files at startup and centralizes access to these settings for consistent configuration management across the application.

## Detailed Code Analysis

### app.py
- **Purpose:**  
  Initializes the application.
- **Key Functionalities:**  
  - Imports configuration data from `utils/config.py`.
  - Initializes core modules, such as AI processing (`operations/ai.py`) and memory management (`operations/memory.py`).
  - Sets up logging, error handling, or routing (if applicable) to link different parts of the application.
  - Includes a main function block (`if __name__ == "__main__":`) to start the application.
- **Design Considerations:**  
  Designed to serve as the orchestrator, keeping the startup logic simple and delegating detailed processing to specialized modules.

### operations/ai.py
- **Purpose:**  
  Contains the algorithms and helper functions for processing text input.
- **Key Functionalities:**  
  - Implements functions (e.g., `generate_response(input_text)`) to interface with AI models.
  - May perform input validation, pre-process data, feed it into an AI model, and post-process the generated response.
  - Includes error handling for cases where the AI model fails or returns unexpected outputs.
- **Design Considerations:**  
  Follows single-responsibility principles to keep AI-specific logic isolated, making it easier to update or swap out the underlying AI engine.

### operations/memory.py
- **Purpose:**  
  Manages conversation history and state across sessions.
- **Key Functionalities:**  
  - Provides functions or classes to store incoming conversation data.
  - Implements retrieval and update functions so that context is maintained during a session.
- **Design Considerations:**  
  Ensures data persistence (if needed) while keeping in-memory operations lightweight and efficient for fast access.

### schemas/schema.py
- **Purpose:**  
  Defines data structures and validation rules.
- **Key Functionalities:**  
  - Uses data classes or schema libraries to define models for inputs and outputs.
  - Enforces type checking and validation to catch errors early and maintain data integrity.
  - Provides transformations between raw data and structured objects that other modules can easily use.
- **Design Considerations:**  
  Aims for clarity and robustness in handling data across different layers of the application, making debugging and maintenance easier.

### utils/config.py
- **Purpose:**  
  Centralizes configuration settings for the entire project.
- **Key Functionalities:**  
  - Reads data from environment variables or external configuration files.
  - Provides helper functions to access configuration parameters (e.g., API keys, debug modes, etc.).
  - May define default values for configuration items to ensure the application can run in different environments.
- **Design Considerations:**  
  Focuses on simplifying access to configuration data, reducing repetition and potential errors in configuration retrieval across different modules.

### utils/__init__.py
- **Purpose:**  
  Initializes the utils package and exposes utility functions to other parts of the application.
- **Key Functionalities:**  
  - May import and re-export functions from `config.py` or other utility modules to provide a single import point.
- **Design Considerations:**  
  Keeps the utility functions organized, making them easily accessible and promoting reuse throughout the project.

## Databases
This application uses two databases for different purposes:
- Qdrant: A vector database utilized for storing and retrieving embeddings.
- history.db: A SQLite database that retains conversation history and memory texts.

## Configuration
Before running the application, ensure that your environment variables are correctly set up:
1. Copy the .env.example file to a new file named .env.
2. Open .env and replace the placeholder API_KEY value ("GEMINI_API_KEY") with your actual Gemini API key.
Adjust settings and configurations as needed by editing `utils/config.py`.

## Installation

```bash
git clone https://github.com/MesutHakanTaskiner/AI_Chatbot_With_LTM.git
```

## Usage (without Docker)
To run the application without Docker, follow these steps:

1. Ensure you have Python 3.x installed.

2. Create a virtual environment (for Windows):
   ```bash
   python -m venv chatbot
   chatbot\Scripts\activate
   ```
   (Ensure that the virtual environment is activated before proceeding.)
3. Install dependencies within the activated environment:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Configure your environment variables:
   Copy the `.env.example` file to a new file named `.env` and update it with your settings.
5. Run the application:
   ```bash
   python app.py
   ```


## Docker
This project can be run inside a Docker container. The provided Dockerfile (and its duplicate "dockerfile") uses the python:3.11-slim image to create a lightweight container. It sets the working directory to /app, installs dependencies from requirements.txt, copies the project files, and runs the application with uvicorn on port 8000.

Using Docker Compose:
1. Run the service with:
  ```bash
   docker-compose up --build
  ```
2. If docker build exists:
  ```bash
   docker-compose up
  ```

This docker-compose configuration maps the current directory to /app in the container, allowing changes to be reflected immediately.

If you are using environment variables, uncomment the relevant COPY command for .env in the Dockerfile.


## Frontend Access
Users can reach the frontend via:
- http://0.0.0.0:8000
- http://127.0.0.1:8000