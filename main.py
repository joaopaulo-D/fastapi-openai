import openai
from dotenv import dotenv_values
from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()
config = dotenv_values(".env")
openai.api_key = config["OPENAI_KEY"]


class Chat(BaseModel):
    role: str
    content: str


@app.get("/api/chat/test")
def test():
  messages = [
    {"role": "user", "content": "O que é IA?"},
  ]
  response = openai.ChatCompletion.create(
    model=config["MODEL"], messages=messages, max_tokens=int(config["MAX_TOKENS"])
  )
  return {
    "data": {
      "id": response.id,
      "created": response.created,
      "message": response.choices[0].message,
    }
  }


@app.post("/api/chat/")
def send(data: Chat):
  response = openai.ChatCompletion.create(
    model=config["MODEL"],
    messages=[{"role": data.role, "content": data.content}],
    max_tokens=int(config["MAX_TOKENS"]),
  )

  return {
    "data": {
      "id": response.id,
      "created": response.created,
      "message": response.choices[0].message,
    }
  }
