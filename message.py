#code_gen_prefix = "You are a senior programmer. Write a javascript code that "
#code_gen_suffix = ". Write the code only without any explanation"
code_gen_prefix = "write a pure JavaScript code snippet that "
code_gen_suffix = " in the web page. Write answer in Markdown without any explanation, html elements"
valid_prefix = " What does following javascript code is doing "
valid_suffix = "  "
valid_suffix2 = ""

realization_prefix = "You are the best business analyst who works in agile methodolgy. You are excellent to express the vague idea of your client as a user scenario. \
After reading your user scenario, the project owner understand clearly what you want them to build.\
Here is the client's idea:\n\n"

realization_suffix = "\n\n\
And here is the criterias to include to describe the idea as a user scenario:\
\
Context: Describe the situation and steps your actual user takes to arrive at your product/service\
Goals: What do they want to achieve?\
Problems: What are they trying to solve and what obstacles do they encounter?\
User motivations: Why do they need or want your offering?\
Personal traits: Provide background to paint a more detailed picture\
Relevant habits, hobbies, and/or beliefs: Actions and emotions that occur in relation to your product/service add a layer of context. \
Write your text as a snake case json to export for agile software automatically. No explanation.\n\n\
Here is the typescript data parameters that agile project management expects to receive:\n\n\
\
typeFlowStep={'step':number,'action':string,'description':string};typeRealizationTemplate={'title':string;context:{user:string,background:string,steps:string[]},goals:string[],problems:[{description:string,obstacles:string[]}],'user_motivations':string[],'personal_traits':string[],'relevant_habits_hobbies_beliefs':string[],'user_scenario_flow':FlowStep[]};"


class Answer():
    code: str | None = ""
    answer: any = None
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
    return answer

def clean_code(raw: str) -> str:
    raw = raw.replace("```javascript", "").replace("```", "").replace("<script>", "").replace("</script>", "")
    raw = raw.replace("\n", "")
    if (raw.startswith("json")):
        return raw[4:]
    return raw

def code_prompt(code_gen_task: str) -> str:
    return code_gen_prefix + code_gen_task + code_gen_suffix 

def validate_prompt(task: str, code: str) -> str:
    return valid_prefix + clean_code(code) + valid_suffix + valid_suffix2

def realization_prompt(idea: str) -> str:
    return realization_prefix + idea + realization_suffix