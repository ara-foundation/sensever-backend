Start virtual environment. In the virtual environment download the packages using pip:

`python -m pip install -r requirements.txt`

Download the model from https://gpt4all.io/index.html.
Put the downloaded model in the `models` directory, then edit the `main.py` to choose your desired model.

Finally run the server:

```shell
uvicorn main:app --host 0.0.0.0 --port 8088
```