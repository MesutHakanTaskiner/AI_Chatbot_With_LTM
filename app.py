"""Main FastAPI application for handling routes and integrating AI operations.
This module sets up routes for asking questions, deleting sessions, and modifying system instructions.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from ai_operations import AiOperations

app = FastAPI()
templates = Jinja2Templates(directory="templates")
ai_ops = AiOperations()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "")
    session_id = data.get("session", None)

    print(f"Question: {question}, Session: {session_id}")

    response = ai_ops.get_answer(question, session_id)

    return JSONResponse(content={"response": response, "session": session_id})


@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    ai_ops.delete_session_thread(session_id)
    print(f"Session {session_id} deleted")
    return JSONResponse(content={"status": "deleted", "session_id": session_id})


@app.post("/set_system_instruction")
async def system_instruction(request: Request):
    data = await request.json()
    instruction = data.get("instruction")
    ai_ops.set_system_instruction(instruction)
    return JSONResponse(content={"status": "success", "message": "System instruction received"})


@app.get("/get_system_instruction")
async def get_system_instruction():
    return JSONResponse(content={"system_instruction": ai_ops.get_system_instruction()})

@app.get("/get_memory")
async def get_memory():
    print("Memory requested")
    memory_data = ai_ops.get_memory()
    return JSONResponse(content={"memory": memory_data})


@app.post("/update_memory")
async def update_memory(request: Request):
    data = await request.json()
    key = data.get("key")
    new_value = data.get("new_value")
    result = ai_ops.update_memory(key, new_value)
    return JSONResponse(content={"status": "success", "message": "Memory updated", "result": result})

@app.post("/delete_memory")
async def delete_memory(request: Request):
    data = await request.json()
    key = data.get("key")
    result = ai_ops.delete_memory(key)
    return JSONResponse(content={"status": "success", "message": "Memory deleted", "result": result})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
