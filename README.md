A Sensever virtual assistant's backend. Sensever is a virtual assistant in the Ara project.
Please refer to `ara` for more information about the Sensever context.

Currently Sensever background several models: Mistral, Open Interpreter and Gpt4All.

# Setup

Start virtual environment. In the virtual environment download the packages using pip:

`python -m pip install -r requirements.txt`


Finally run the server:

```shell
uvicorn mistral:app --host 0.0.0.0 --port 8088
```
# Mistral
Directly using the fast Mistral API

# Open Interpreter
Open Interpreter is a AI interface to your computer. Control your computer using AI.

---
# Gpt4All
Gpt4All is a software project that allows to run Large Language Models (LLMs) on your computer offline.
Large Language Models are type of Machine Learning softwares that generate a text for the user's prompt.

The most popular LLM is ChatGPT from OpenAI.

First, install gpt4all:
```
python -m pip install gpt4all
```

Prepare the model:
1. Download the model from https://gpt4all.io/index.html.
2. Put the downloaded model in the `models` directory, then edit the `gpt4all.py` to choose your desired model.


Then run the gpt4all package:

```
uvicorn gpt4all:app --host 0.0.0.0 --port 8088
```