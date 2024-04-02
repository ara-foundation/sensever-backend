#code_gen_prefix = "You are a senior programmer. Write a javascript code that "
#code_gen_suffix = ". Write the code only without any explanation"
code_gen_prefix = "write a pure JavaScript code snippet that "
code_gen_suffix = " in the web page. Write answer in Markdown without any explanation, html elements"
valid_prefix = " What does following javascript code is doing "
valid_suffix = "  "
valid_suffix2 = ""

class Answer():
    code: str | None = ""
    correct: bool
    error: str | None

def wrong_answer(error: str | None) -> Answer:
    answer = Answer()
    answer.correct = False
    answer.error = error
    answer.code = ""
    return answer

def correct_answer(code: str) -> Answer:
    answer = Answer()
    answer.correct = True
    answer.code = clean_code(code)
    return answer

def clean_code(raw: str) -> str:
    return raw.replace("```javascript", "").replace("```", "").replace("<script>", "").replace("</script>", "")

def code_prompt(code_gen_task: str) -> str:
    return code_gen_prefix + code_gen_task + code_gen_suffix 

def validate_prompt(task: str, code: str) -> str:
    return valid_prefix + clean_code(code) + valid_suffix + valid_suffix2

