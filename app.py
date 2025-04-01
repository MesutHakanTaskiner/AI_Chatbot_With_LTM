"""Main FastAPI application for handling AI operations via HTTP REST endpoints.

This module initializes the FastAPI application, sets up route handlers for various API endpoints,
such as asking questions, managing session threads, configuring system instructions, and handling memory operations.
It integrates with AiOperations defined in operations/ai.py.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from operations.ai import AiOperations
from contextlib import asynccontextmanager

# Initialize FastAPI app

# Setup Jinja2 templates directory for rendering HTML pages
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ai_ops = AiOperations()
    yield  # app runs here
    # You can add cleanup logic after yield if needed (e.g., closing DB connections)


app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Renders the index page.

    Parameters:
    - request (Request): The incoming HTTP request object.

    Returns:
    - HTMLResponse: The rendered HTML page using the 'index.html' template.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_question(request: Request):
    """
    Handles the '/ask' endpoint to process a user's question.

    The request should be a JSON containing:
    - 'question': The question asked by the user.
    - 'session': The session identifier.

    It calls the AiOperations.get_answer method to generate a response and optionally context.

    Returns:
    - JSONResponse: A JSON object containing the response, session id, and context if available.
    """
    data = await request.json()
    question = data.get("question", "")
    session_id = data.get("session", None)
    # Process the question with AI operations
    response, context = app.state.ai_ops.get_answer(question, session_id)
    if context != "":
        return JSONResponse(content={"response": response, "session": session_id, "context": context})
    else:
        return JSONResponse(content={"response": response, "session": session_id})

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Deletes the message thread associated with a given session.

    Parameters:
    - session_id (str): The identifier for the session to delete.

    Returns:
    - JSONResponse: A confirmation message with session id.
    """
    app.state.ai_ops.delete_session_thread(session_id)
    print(f"Session {session_id} deleted")
    return JSONResponse(content={"status": "deleted", "session_id": session_id})

@app.post("/set_system_instruction")
async def system_instruction(request: Request):
    """
    Sets the system instruction for the AI operations.

    The JSON request should contain:
    - 'instruction': The new system instruction to be set.

    Returns:
    - JSONResponse: A confirmation message after updating the system instruction.
    """
    data = await request.json()
    instruction = data.get("instruction")
    app.state.ai_ops.set_system_instruction(instruction)
    return JSONResponse(content={"status": "success", "message": "System instruction received"})

@app.get("/get_system_instruction")
async def get_system_instruction():
    """
    Retrieves the current system instruction.

    Returns:
    - JSONResponse: A JSON object with the current system instruction.
    """
    return JSONResponse(content={"system_instruction": app.state.ai_ops.get_system_instruction()})

@app.get("/get_memory")
async def get_memory():
    """
    Retrieves stored memory data from the AI operations.

    Returns:
    - JSONResponse: A JSON object containing memory data.
    """
    memory_data = app.state.ai_ops.get_memory()
    print(f"Memory data: {memory_data}, type: {type(memory_data)}")
    return JSONResponse(content={"memory": memory_data})

@app.post("/update_memory")
async def update_memory(request: Request):
    """
    Updates a memory entry.

    The request JSON should include the update data containing keys such as 'old_value' and 'new_value'.

    Returns:
    - JSONResponse: A confirmation message with result of the update.
    """
    data = await request.json()
    result = app.state.ai_ops.update_memory(data)
    return JSONResponse(content={"status": "success", "message": "Memory updated", "result": result})

@app.post("/delete_memory")
async def delete_memory(request: Request):
    """
    Deletes a memory entry.

    The request JSON should include the key 'value' specifying which memory to delete.

    Returns:
    - JSONResponse: A confirmation message with result of the deletion.
    """
    data = await request.json()
    result = app.state.ai_ops.delete_memory(data)
    return JSONResponse(content={"status": "success", "message": "Memory deleted", "result": result})

if __name__ == "__main__":
    """
    Starts the FastAPI application using uvicorn when the script is run directly.
    
    The application is served on host '127.0.0.1' and port 8000 with auto-reload enabled.
    """
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
