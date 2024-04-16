import subprocess
from ast import literal_eval
import json
import pandas as pd
import re
from openai import OpenAI

from api_key import API_KEY

survey = "ANES"
model = "gpt-3.5-turbo-0125"

if survey == "ANES":
    query = "In the 2020 presidential election, (1) Joe Biden is the Democratic candidate, "
    query += "and (2) Donald Trump is the Republican candidate, and I voted for"
    coln = "VCF0705"
if survey == "CSEE":
    query = "If a federal election were held in 2022, between (1) left wing parties (Green, NDP, Liberals), "
    query += "and (2) right wing parties (Conservatives, PPC), I would be mostly like to vote for"
    coln = "fed_vote2" #fed_vote - parties directly, make sure to also change the prompt above ^

with open(survey + "/results/personas.json", 'r') as f:
    personas = json.load(f)
with open(survey + "/editedSurvey/survey_questions.json", 'r') as f:
    survey_questions = json.load(f)

""" TO GET A SUBSET OF PERSONAS """
# personas_keys = []
# for i in range(64876, 68224):
#     personas_keys.append(str(i))
# personas = {k: personas[k] for k in personas_keys}

client = OpenAI(api_key=API_KEY)

requests = []
for responseID in personas:
    requests.append({
        "messages": [{
            "role": "user",
            "content": personas[responseID] + "\n" + query + "\n" + "Respond with only the number corresponding to the answer.",
        }],
        "model": model,
        "metadata": {"responseID": responseID}
    })

with open("tmp/requests.jsonl", "w") as f:
    for job in requests:
        json_string = json.dumps(job)
        f.write(json_string + "\n")

with open("tmp/results.jsonl", "w") as f:
    f.write("")

cmd = "python3 api_request_parallel_processor.py "
cmd += "--requests_filepath tmp/requests.jsonl "
cmd += "--save_filepath tmp/results.jsonl "
cmd += "--request_url https://api.openai.com/v1/chat/completions "
cmd += "--api_key " + API_KEY + " "
cmd += "--logging_level 20"

subprocess.call(cmd, shell=True)

def parse(answer, responseID):
    answer = answer.strip()
    if answer.isnumeric():
        return answer
    elif answer[0].isnumeric():
        return answer[0]
    elif bool(re.match(r"^\([1-9]\)", answer)): # (2) Republican
        return answer[1]
    elif bool(re.match(r"^- [1-9]", answer)): # - 2
        return answer[2]
    else:
        print("Received a non-parsable response for responseID " + responseID)
        print("Response: <start>" + answer + "<end>")

responses = []
with open("tmp/results.jsonl", "r") as f:
    for request in f:
        request = request.replace("null", "None")
        request = literal_eval(request)
        response = {"responseID": request[2]["responseID"]}
        response[coln] = parse(request[1]["choices"][0]["message"]["content"], response["responseID"])
        responses.append(response)

df = pd.DataFrame(responses)
df.to_csv(survey + "/results/ss_responses.csv", index=False)