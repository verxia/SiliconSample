from math import isnan
import pandas as pd
import json
import construct_personas

survey = "ANES"
eval_number = 1

human_responses = pd.read_csv(survey + "/editedSurvey/human_responses.csv") 
ss_responses = pd.read_csv(survey + "/results/ss_responses.csv")

eval_folder_filepath = survey + "/results/evaluation/attempt_" + str(eval_number) + ".csv"
eval_notes_filepath = survey + "/results/notes.txt"

if survey == "ANES":
    coln = "VCF0705"
    key = "Key:\n1: Democrat\n2: Republican\n3: Other"
    number_of_options = 3
if survey == "CSEE":
    coln = "fed_vote2"
    key = "Key:\n1: Left wing parties (Green, NDP, Liberals)\n2: Right wing parties (Conservatives, PPC)"
    number_of_options = 2

with open(survey + "/results/personas.json", 'r') as f:
    personas = json.load(f)

evaluation = { "responseID": [], "persona": [], "human": [], "ss": []}

correct = 0
total = 0
invalid_ss = 0
for _, ss_row in ss_responses.iterrows():
    human_row = human_responses.loc[human_responses['responseID'] == ss_row["responseID"]]

    evaluation["responseID"].append(ss_row["responseID"])
    evaluation["persona"].append(personas[str(int(ss_row["responseID"]))])
    evaluation["human"].append(human_row.iloc[0][coln])
    evaluation["ss"].append(ss_row[coln])

    if isnan(ss_row[coln]) or ss_row[coln] not in range(1, number_of_options+1) or ss_row[coln] not in range(1, number_of_options+1):
        invalid_ss += 1
        continue
    if int(human_row.iloc[0][coln]) != 1 and int(human_row.iloc[0][coln]) != 2 and int(human_row.iloc[0][coln]) != 3:
        continue
    if int(human_row.iloc[0][coln]) == int(ss_row[coln]):
        correct += 1
    total += 1


evaluation = pd.DataFrame(evaluation)
evaluation.to_csv(eval_folder_filepath, index=False)

result = "\n\n## ATTEMPT " + str(eval_number) + "\n"
result += str(construct_personas.questions) + "\n"
result += "--------------------------------------------------------------\n"
result += "Percent correct: " + str(round(correct/total*100, 2)) + "%\n"
result += "--------------------------------------------------------------\n"

confusion_matrix = {}
for i in range(1, number_of_options+1):
    confusion_matrix["human_" + str(i)] = {}
    for j in range(1, number_of_options+1):
        confusion_matrix["human_" + str(i)]["ss_" + str(j)] = 0
    confusion_matrix["human_" + str(i)]["human_total"] = 0
confusion_matrix["ss_total"] = {}
for j in range(1, number_of_options+1):
    confusion_matrix["ss_total"]["ss_" + str(j)] = 0
confusion_matrix["ss_total"]["human_total"] = 0

for index, ss_row in ss_responses.iterrows():
    if isnan(ss_row[coln]) or ss_row[coln] not in range(1, number_of_options+1) or ss_row[coln] not in range(1, number_of_options+1):
        continue
    human_row = human_responses.loc[human_responses['responseID'] == ss_row["responseID"]]
    h = int(human_row.iloc[0][coln])
    s = int(ss_row[coln])
    if h not in range(1, number_of_options+1) or s not in range(1, number_of_options+1):
        continue
    confusion_matrix["human_" + str(h)]["ss_" + str(s)] += 1
    confusion_matrix["ss_total"]["ss_" + str(s)] += 1
    confusion_matrix["human_" + str(h)]["human_total"] += 1 
    confusion_matrix["ss_total"]["human_total"] += 1

if invalid_ss != 0:
    result += "Generated " + str(invalid_ss) + " invalid responses\n"
result += pd.DataFrame.from_dict(confusion_matrix).to_string()
result += "\n--------------------------------------------------------------\n"
result += key

with open (eval_notes_filepath, 'a') as f:
    f.write(result)
