# interpreter.py
from dotenv import load_dotenv
load_dotenv()
from lmdbm import Lmdb

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import message
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import json
import requests

api_key = os.getenv("MISTRAL_API_KEY")
ara_url = os.getenv("ARA_SERVER_URL")
model = "mistral-large-latest" # Largest, and best, but paid :(
# model = "pixtral-12b-2409" # Largest, recent free model

print(ara_url)
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
        json.loads(output)
        result.correct = True
    except:
        result.correct = False

    return result

# The request must have the following POST body in the JSON format:
# id - an id of the post issued by the Ara Forum
# requester - a username signed up on the Ara Forum
# content - a string represantion of the idea post
@app.post("/scenario-draft")
async def realization_type(request: Request):
    idea = await request.json();
    if 'content' not in idea or 'requester' not in idea or 'token' not in idea or 'id' not in idea:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"correct": False, "message": "no valid parameters"})

    prompt = message.realization_prompt(idea['content'])

    # Validate the token
    r = requests.post(ara_url + '/users/valid-token', json={'token': idea['token']})
    if r.status_code != 200:
        print(r.text)
        print(r.status_code)
        print(ara_url + '/users/valid-token')
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"correct": False, "message": "server error"})
    validation_result = r.json()
    if validation_result['valid'] == False:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"correct": False, "message": "invalid token"})

    print("Later prevent unathorized users from entering into this page")
    print("Scenario Draft was requested for " + str(idea['id']) + " by " + idea['requester'])

    key = "draft_" + str(idea['id'])

    with Lmdb.open("mistral_scenario_drafts.db", "c") as db:
        obj = db.get(key)
        if obj is not None:
            result = message.correct_answer(obj)
            print("the " + key + " exists in the cache. return it")
            result.answer = json.loads(obj)
            result.correct = True
            return result
        else:
            print("the " + key + " doesn't exist in the cache. Let's generate it")

    response = client.chat(
        model=model,
        messages=[ChatMessage(role="user", content=prompt)],
    )
    output = message.clean_code(response.choices[0].message.content)

    result = message.correct_answer(output)

    try:
        result.answer = json.loads(output)
        result.correct = True
        with Lmdb.open("mistral_scenario_drafts.db", "c") as db:
            db.update({key: output})
            print("the " + key + " was saved in the cache")
    except:
        result.correct = False

    return result