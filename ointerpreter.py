# interpreter.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from interpreter import interpreter
import message
from datetime import datetime

interpreter.llm.model = "mistral/mistral-tiny"
interpreter.llm.max_tokens = 4096
interpreter.llm.context_window = 2048
interpreter.system_message = ""

app = FastAPI()

@app.get("/")
async def root():
    return message.correct_answer("")

@app.get("/chat")
def chat_endpoint(message: str):
    def event_stream():
        for result in interpreter.chat(message, stream=True):
            yield f"data: {result}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/history")
def history_endpoint():
    return interpreter.messages

@app.get("/implement")
def add(code_gen_task: str):
    interpreter.message = []
    code_prompt = message.code_prompt(code_gen_task)

    print("Code to write ", code_prompt)
    print("generating code... at = ", datetime.now().strftime("%H:%M:%S"))

    output = interpreter.chat(code_prompt)

    print("generated ", datetime.now().strftime("%H:%M:%S"))
    print(output)

    validate_prompt = message.validate_prompt(output)

    print("validating code... at = ", datetime.now().strftime("%H:%M:%S"))
    print(validate_prompt)

    validate_output = interpreter.chat(validate_prompt)

    print("validated: ", datetime.now().strftime("%H:%M:%S"))
    print(validate_output.lower())

    result = message.correct_answer(output)

    if (validate_output.lower().find("yes")):
        result.correct = True
    else:
        result.correct = False

    return result