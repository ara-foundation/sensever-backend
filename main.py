from gpt4all import GPT4All
from datetime import datetime
from fastapi import FastAPI
from pathlib import Path
import time

app = FastAPI()

cwd = Path.cwd()

path = cwd.joinpath("./models/mistral-7b-instruct-v0.1.Q4_0.gguf")
code_gen_prefix = "You are a senior programmer. "
code_gen_suffix = " is a programming task to complete. Write a javascript code without explanation."
valid_prefix = "you are a senior programmer. You receive a question to answer: "
valid_suffix = " write 'yes' or 'no' without any explanation"

print(str(path))

model = GPT4All(str(path), n_threads=8, ngl=32)

@app.get("/")
async def root():
    return {"correct": True}

@app.get("/implement")
def add(code_gen_task: str):
    #time.sleep(3)
    #result = {
    #    "code":"\n```javascript\nfunction changeBackgroundColor(color) {\n  document.body.style.backgroundColor = color;\n}\n\nchangeBackgroundColor('red');\n```".replace("```javascript", "").replace("```", ""),
    #    "correct": True
    #}
    #return result
    task = code_gen_prefix + code_gen_task + code_gen_suffix 

    print("generating code... at = ", datetime.now().strftime("%H:%M:%S"))

    output = model.generate(task, max_tokens=4096, temp=0.7, top_k=40, repeat_penalty=1.18, top_p=0.4, n_batch=128)

    print("generated ", datetime.now().strftime("%H:%M:%S"))
    print(output)

    valid_task = output.replace("```javascript", "'").replace("```", "'") + " is a complete code snipped for " + code_gen_task + "?"
    valid = valid_prefix + valid_task + valid_suffix

    print("validating code... at = ", datetime.now().strftime("%H:%M:%S"))
    print(valid)
    valid_output = model.generate(valid, max_tokens=4096, n_batch=128, streaming=False)

    print("validated: ", datetime.now().strftime("%H:%M:%S"))
    print(valid_output.lower())

    result = {
        "code": output.replace("```javascript", "").replace("```", ""),
        "correct": True,
    }

    if (valid_output.lower().find("yes")):
        result["correct"] = True
    else:
        result["correct"] = False

    return result