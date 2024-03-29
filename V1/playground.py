import pandas as pd
import json
from openai import OpenAI
from file_paths import *
from ANES_all.editedSurvey.choice_mappings import *



def get_personas():
    personas = []

    for index, row in df.iterrows():
        # Add more demographic information here
        persona = "You " + gender_mapping[row["gender"]] + " and you are " + age_cat_mapping[int(row["age_cat"])] + " years old, living in " + prov_mapping[row["prov"]] + "."
        personas.append(persona)
    
    return personas

def construct_baseline_message():
    message = [
        {
            "role": "system",
            "content": baseline_message 

        },
        {
            "role": "user",
            "content": questions
        }  
    ]

    return [message]
    

def construct_persona_message():
    personas = get_personas()
    messages = []
    for i in range(len(personas)):
        message = [
            {
                "role": "system",
                "content": baseline_message
            },
            {
                "role": "user",
                "content": personas[i] + "\n" + questions
            }  
        ]
        messages.append(message)

    return messages


def runChatGPT(messages, model="gpt-3.5-turbo-1106"):

    client = OpenAI(api_key=API_KEY)
    
    responses = []
    for message in messages:
        response = client.chat.completions.create(
            model=model,
            messages=message,
        )
        responses.append(response.choices[0].message.content)
    return responses

    json_path = "/Users/veronicaxia/Files/School/siliconSamples/survey_questions.json"
    f = open(json_path)
    questions = json.load(f)
    f.close()

    questions_path = "questions.txt"

    with open(questions_path, "r") as f:
        pass
        for line in f:
            print (questions[line.strip("\n")]["question"])

    messages = construct_persona_message()
    responses = runChatGPT(messages)
    print(responses)

def remove_parties():
    human_responses = pd.read_csv(RESPONSES_PATH)
    ss_responses = pd.read_csv(SS_RESPONSES_PATH)

    d = []
    total = 0
    count = 0
    for index, human_row in human_responses.iterrows():  
        parties = ["Democrat", "Republican"]
        if initial_party_mapping[human_row["VCF0302"]] not in parties or vote_mapping[human_row["VCF0705"]] not in parties:
            continue
        if initial_party_mapping[human_row["VCF0302"]] == vote_mapping[human_row["VCF0705"]]:
            continue
        else:
            total += 1
            ss_row = ss_responses.loc[ss_responses['responseID'] == human_row["responseID"]].values
            d.append({"responseID": human_row["responseID"], "initialParty": initial_party_mapping[human_row["VCF0302"]], "humanVote": vote_mapping[human_row["VCF0705"]], "ssVote": vote_mapping[ss_row[0][1]]})
            if vote_mapping[ss_row[0][1]] == vote_mapping[human_row["VCF0705"]]:
                count += 1
    df = pd.DataFrame(d)
    df.to_csv("initial_party_vote_discrepencies.csv", index=False)
    print (count / total)


def filter_anes():
    anes = pd.read_csv("ANES_all/originalSurvey/anes_timeseries_cdf_csv_20220916.csv")
    anes = anes.loc[anes['VCF0004'] == 2020]
    anes = anes[["VCF0101", "VCF0104", "VCF0105a", "VCF0130", "VCF0302", "VCF0310", "VCF0705", "VCF0733", "VCF0305", "VCF0803", "VCF0901b"]]



API_KEY = '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'


if __name__ == "__main__":
    filter_anes()


"""
ChatGPT's baseline
socio_prospective_ 2
financial_worry_ 2
Q_seen_ 1
changes_bad_ 4
fiona_ 1
fiona_attribution_ 5

Male, 6, Manitoba
socio_prospective_ 2
financial_worry_ 2
Q_seen_ 1
changes_bad_ 4
fiona_ 1
fiona_attribution_ 5

Male, 7, Ontario
socio_prospective_ 3
financial_worry_ 2
Q_seen_ 1
changes_bad_ 4
fiona_ 2
fiona_attribution_ 5

Male, 1, Ontario
socio_prospective_3
financial_worry_2
Q_seen_1
changes_bad_4
fiona_2
fiona_attribution_5

Male, 4, Quebec
socio_prospective_3
financial_worry_1
Q_seen_1
changes_bad_2
fiona_2
fiona_attribution_5

Male, 1, Quebec
socio_prospective_ 3
financial_worry_ 1
Q_seen_ 1
changes_bad_ 2
fiona_ 2
fiona_attribution_ 5
"""
