# interpreter.py
from dotenv import load_dotenv
load_dotenv("./env")

from fastapi import FastAPI
import message
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from pyjsparser import parse

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-tiny"

client = MistralClient(api_key=api_key)

app = FastAPI()

@app.get("/")
async def root():
    return message.correct_answer("")

@app.get("/implement")
def add(code_gen_task: str):
    code_prompt = message.code_prompt(code_gen_task)

    code_response = client.chat(
        model=model,
        messages=[ChatMessage(role="user", content=code_prompt)],
    )
    output = message.clean_code(code_response.choices[0].message.content)

    result = message.correct_answer(output)

    try:
        parse(output)
        result.correct = True
    except:
        result.correct = False

    return result