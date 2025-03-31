import os
from mem0 import Memory

os.environ["GEMINI_API_KEY"] = "AIzaSyD09_GL15OALgvia2b4X_Z315nRTV-twI0"

config = {
    "llm": {
        "provider": "litellm",
        "config": {
            "model": "gemini/gemini-2.0-flash",
            "temperature": 0.2,
            "max_tokens": 1500,
        }
    },
    "embedder": {
        "provider": "gemini",
        "config": {
            "model": "models/text-embedding-004",
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "embedding_model_dims": 768,
            "path": os.getcwd() + "/qdrant",
        }
    },
    "history_db_path": "history.db"
}

m = Memory.from_config(config)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello! How are you? My name is Alice."},
    {"role": "assistant", "content": "I'm good, thank you! How can I assist you today?"},
    {"role": "user", "content": "Can you tell me about the weather?"},
    {"role": "assistant", "content": "Sure! What location are you interested in?"},
    {"role": "user", "content": "New York."},
    {"role": "assistant", "content": "The weather in New York is sunny with a high of 75°F."},
    {"role": "user", "content": "Thanks!"},
    {"role": "assistant", "content": "You're welcome! Let me know if you need anything else."},
]

m.add(messages, user_id="alice")

'''import os
from mem0 import Memory

os.environ["OPENAI_API_KEY"] = "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"

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o",
            "temperature": 0.2,
            "max_tokens": 1500,
        }
    }
}

m = Memory.from_config(config)
m.add("Likes to play cricket on weekends", user_id="alice", metadata={"category": "hobbies"})'''