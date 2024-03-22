import json
import pandas as pd
import random
import re
from file_paths import *
from api_key import API_KEY
from openai import OpenAI

def ask(model="gpt-3.5-turbo"):
    with open(PERSONAS_PATH, 'r') as f:
        personas = json.load(f)
    with open(SURVEY_QUESTIONS_PATH, 'r') as f:
        survey_questions = json.load(f)

    # personas_keys = []
    # for i in range(64876, 68224):
    #     personas_keys.append(str(i))
    # personas = {k: personas[k] for k in personas_keys}

    # ranking, multi-select, multiple-choice-scale, multiple-choice, written
    survey_questions =  {k: survey_questions[k] for k in SURVEY_KEYS}

    client = OpenAI(api_key=API_KEY)
    responses = []

    for persona in personas:
        response = {"responseID": persona}
        for question in survey_questions:
            if survey_questions[question]["type"] == "multiple-choice" or survey_questions[question]["type"] == "multiple-choice-scale":
                ask_multiple_choice(client, model, persona, personas[persona], survey_questions[question], response)
            elif survey_questions[question]["type"] == "multi-select":
                ask_multi_select(client, model, persona, personas[persona], survey_questions[question], response)
            elif survey_questions[question]["type"] == "written":
                ask_written(client, model, persona, personas[persona], survey_questions[question], response)
            elif survey_questions[question]["type"] == "ranking":
                ask_ranking(client, model, persona, personas[persona], survey_questions[question], response)
            else:
                raise Exception("Question type " + question["type"] + " is not implemented." )
        
        responses.append(response)
    
        df = pd.DataFrame(responses)
        df.to_csv(SS_RESPONSES_PATH, index=False)

def ask_multiple_choice(client, model, responseID, persona, question_info, response):

    question = question_info["question"]
    coln = question_info["colns"][0]

    answer = client.chat.completions.create(
        model = model,
        messages = [
            {
                "role": "user",
                "content": "Adopt the following persona and answer the question.\n" + persona + "\n" + question + "\n" + "Respond with only the number corresponding to your answer."
            }
        ],
    )
    answer = answer.choices[0].message.content.strip()
    if answer.isnumeric():
        response[coln] = answer
    elif bool(re.match(r"^\([1-9]\)", answer)): # (2) Republican
        response[coln] = answer[1]
    elif bool(re.match(r"^[1-9]\.", answer)): # 1. Democrat
        response[coln] = answer[0]
    elif bool(re.match(r"^[1-9][ ]*-", answer)): # 1 - Democrat
        response[coln] = answer[0]
    elif bool(re.match(r"^[1-9][ ]", answer)): # 2 (Republican)
        response[coln] = answer[0]
    elif bool(re.match(r"^[1-9]\)", answer)): # 1) Democrat
        response[coln] = answer[0]
    elif bool(re.match(r"^[1-9],", answer)): # 1, Democrat
        response[coln] = answer[0]
    else:
        print("Received a non-parsable response for a multiple choice question with column " + coln + " and responseID " + responseID)
        print("Response: " + answer)
        # extracted_answer = answer.split("(")[1][:len(answer.split("(")[1])-1]
        # print("Extracted answer: " + extracted_answer)
        # if extracted_answer.isnumeric():
        #     response[coln] = extracted_answer
        #     print("Extacted answer included")

def ask_multi_select(client, model, responseID, persona, question_info, response):
    question = question_info["question"]
    colns = question_info["colns"]

    answer = client.chat.completions.create(
        model = model,
        messages = [
            {
                "role": "user",
                "content": persona + "\n" + question + "\n" + "Respond with only the number corresponding to your answer, separated by commas."
            }
        ],
    )

    answer = answer.choices[0].message.content
    answer_list = answer.split(",")

    for i in range(len(answer_list)):
        answer_list[i] = answer_list[i].strip()
        if not answer_list[i].isnumeric():
            print("Received a non-numeric response for a multi-select question with columns " + str(colns) + " and responseID " + responseID)
            print("Response: " + answer)
            return

    for coln in colns:
        if coln[len(coln)-1] in answer_list:
            response[coln] = 1
        else:
            response[coln] = "."

def ask_written(client, model, responseID, persona, question_info, response):
    question = question_info["question"]
    coln = question_info["colns"][0]

    answer = client.chat.completions.create(
        model = model,
        messages = [
            {
                "role": "user",
                "content": persona + "\n" + question
            }
        ],
    )

    response[coln] = answer.choices[0].message.content

def ask_ranking(client, model, responseID, persona, question_info, response):
    question = question_info["question"]
    colns = question_info["colns"]

    answer = client.chat.completions.create(
        model = model,
        messages = [
            {
                "role": "user",
                "content": persona + "\n" + question + "\n" + "In order of your ranking, list each answer using only its number (not the entire answer description), separated by commas."
            }
        ],
    )

    answer = answer.choices[0].message.content
    answer_list = answer.split(",")

    for i in range(len(answer_list)):
        answer_list[i] = answer_list[i].strip()
        if not answer_list[i].isnumeric():
            print("Received a non-numeric response for a ranking question with columns " + str(colns) + " and responseID " + responseID)
            print("Response: " + answer)
            return

    question_key = colns[0][:len(colns[0])-1]
    for i in range(len(answer_list)):
        response[question_key+answer_list[i]] = i + 1

if __name__ == "__main__":
    ask()
