from math import isnan
import pandas as pd

survey = "CSEE"

human_responses = pd.read_csv(survey + "/editedSurvey/human_responses.csv") 
ss_responses = pd.read_csv(survey + "/results/ss_responses.csv")

if survey == "ANES":
    coln = "VCF0705"
    key = "Key:\n1: Democrat\n2: Republican\n3: Other"
    number_of_options = 3
if survey == "CSEE":
    coln = "fed_vote"
    key = "Key:\n1: Left wing parties (Green, NDP, Liberals)\n2: Right wing parties (Conservatives, PPC)"
    number_of_options = 2

correct = 0
total = 0
invalid_ss = 0
for _, ss_row in ss_responses.iterrows():
    if isnan(ss_row[coln]) or ss_row[coln] not in range(1, number_of_options+1) or ss_row[coln] not in range(1, number_of_options+1):
        invalid_ss += 1
        continue
    human_row = human_responses.loc[human_responses['responseID'] == ss_row["responseID"]]
    if int(human_row.iloc[0][coln]) != 1 and int(human_row.iloc[0][coln]) != 2 and int(human_row.iloc[0][coln]) != 3:
        continue
    if int(human_row.iloc[0][coln]) == int(ss_row[coln]):
        correct += 1
    total += 1

print ("--------------------------------------------------------------")
print ("Percent correct:", str(round(correct/total*100, 2)) + "%")
print ("--------------------------------------------------------------")

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
    print ("Generated", invalid_ss, "invalid responses")
print (pd.DataFrame.from_dict(confusion_matrix))
print ("--------------------------------------------------------------")
print(key)