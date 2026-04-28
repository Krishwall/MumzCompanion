from fastapi import FastAPI
from pydantic import BaseModel
from agent.agent import run_agent

app = FastAPI()

class UserRequest(BaseModel):
    user_input: str
    date_input: str

@app.post("/recommend")
def recommend(data: UserRequest):
    return run_agent(data.user_input, data.date_input)
@app.get("/")
def root():
    return {"message": "MumzCompanion API is running 🚀"}