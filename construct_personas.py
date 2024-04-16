import pandas as pd
import json

survey = "ANES"
questions = ["race", "gender", "age", "lib_cons", "interest", "church", "discuss", "postal"]

if survey == "ANES":
    from ANES.editedSurvey.answer_mappings import answer_mappings

if survey == "CSEE":
    from CSEE.editedSurvey.answer_mappings import answer_mappings

responses = pd.read_csv(survey +"/editedSurvey/human_responses.csv")
with open(survey + "/editedSurvey/survey_questions.json", 'r') as f:
    survey_questions = json.load(f)

personas = {}
for _, row in responses.iterrows():
    persona = ""
    for question in questions:
        template = survey_questions[question]["template"]
        colns = survey_questions[question]["colns"]
        mapping = answer_mappings[question]
        question_type = survey_questions[question]["type"]

        if question_type == "multiple-choice":
            if survey == "ANES" and question == "postal":
                persona += template.replace("XXX", mapping[row[colns[0]]]) + " "
                continue
            if row[colns[0]] in [".", 97, 98, "97", "98"] or mapping[int(row[colns[0]])] == "":
                continue
            persona += template.replace("XXX", mapping[int(row[colns[0]])]) + " "
        
        elif question_type == "multi-select":
            choices = ""
            for i, coln in enumerate(colns):
                if row[coln] == "1":
                    choices += mapping[i+1] + ", "
            if choices == "":
                continue
            persona += template.replace("XXX", choices[:-2]) + " "

    personas[row['responseID']] = persona

with open(survey + "/results/personas.json", 'w') as fp:
    json.dump(personas, fp, indent=4)


