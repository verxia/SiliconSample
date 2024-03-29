import json
import pandas as pd
from file_paths import *

def evaluate():
    human_responses = pd.read_csv(RESPONSES_PATH)  
    ss_responses = pd.read_csv(SS_RESPONSES_PATH)

    with open(SURVEY_QUESTIONS_PATH, 'r') as f:
        survey_questions = json.load(f)
    survey_questions =  {k: survey_questions[k] for k in SURVEY_KEYS}

    evaluations = []

    mc_correct = 0
    mc_total = 0
    for index, ss_row in ss_responses.iterrows():
        evaluation = {"responseID": ss_row["responseID"]}
        human_row = human_responses.loc[human_responses['responseID'] == ss_row["responseID"]]
        for question in survey_questions:
            colns = survey_questions[question]["colns"]
            if survey_questions[question]["type"] == "multiple-choice":
                if evaluate_multiple_choice(human_row.iloc[0][colns[0]], ss_row[colns[0]], colns[0], evaluation):
                    mc_correct += 1
                mc_total += 1
            elif survey_questions[question]["type"] == "multiple-choice-scale":
                evaluate_multiple_choice_scale(human_row.iloc[0][colns[0]], ss_row[colns[0]], colns[0], evaluation)
            elif survey_questions[question]["type"] == "written":
                evaluate_written(human_row[colns[0]], ss_row[colns[0]], evaluation)
            elif survey_questions[question]["type"] == "multi-select":
                evaluate_multi_select(human_row, ss_row, colns, evaluation)
            elif survey_questions[question]["type"] == "ranking":
                evaluate_ranking(human_row, ss_row, colns, evaluation)
            else:
                raise Exception("Question type " + question["type"] + " is not implemented." )
        
        evaluations.append(evaluation)
    
    input("This will overwrite the file " + EVALUATIONS_PATH + ". Press enter to proceed.")
    df = pd.DataFrame(evaluations)
    df.to_csv(EVALUATIONS_PATH, index=False)

    return mc_correct/mc_total

#TODO: Add cases if human chose not to answer
    
def evaluate_multiple_choice(human_response, ss_response, coln, evaluation):
    evaluation[coln] = 1 if int(human_response) == int(ss_response) else 0
    return int(human_response) == int(ss_response)

def evaluate_multiple_choice_scale(human_response, ss_response, coln, evaluation):
    evaluation[coln] = abs(int(human_response) - int(ss_response)) if (human_response != "." and ss_response != ".") else -1
    #TODO: normalize answer

def evaluate_multi_select(human_row, ss_row, colns, evaluation):
    for coln in colns:
        evaluation[coln] = 1 if str(human_row.iloc[0][coln]) == str(ss_row[coln]) else 0

def evaluate_written(human_response, ss_response, evaluation):
    return ""

def evaluate_ranking(human_row, ss_row, colns, evaluation):
    for coln in colns:
        evaluation[coln] = 1 if str(human_row.iloc[0][coln]) == str(ss_row[coln]) else 0


def create_confusion_matrix(n):
    human_responses = pd.read_csv(RESPONSES_PATH)  
    ss_responses = pd.read_csv(SS_RESPONSES_PATH)

    with open(SURVEY_QUESTIONS_PATH, 'r') as f:
        survey_questions = json.load(f)
    survey_questions =  {k: survey_questions[k] for k in SURVEY_KEYS}

    confusion_matrix = {}
    for i in range(1, n+1):
        confusion_matrix["human_" + str(i)] = {}
        for j in range(1, n+1):
            confusion_matrix["human_" + str(i)]["ss_" + str(j)] = 0
        confusion_matrix["human_" + str(i)]["human_total"] = 0

    confusion_matrix["ss_total"] = {}
    for j in range(1, n+1):
        confusion_matrix["ss_total"]["ss_" + str(j)] = 0
    confusion_matrix["ss_total"]["human_total"] = 0

    uncounted = 0
    for index, ss_row in ss_responses.iterrows():
        human_row = human_responses.loc[human_responses['responseID'] == ss_row["responseID"]]
        for question in survey_questions:
            colns = survey_questions[question]["colns"]
            h = human_row.iloc[0][colns[0]]
            s = ss_row[colns[0]]
            if h not in range(1, n+1) or s not in range(1, n+1):
                uncounted += 1
                continue
            confusion_matrix["human_" + str(h)]["ss_" + str(s)] += 1
            confusion_matrix["ss_total"]["ss_" + str(s)] += 1
            confusion_matrix["human_" + str(h)]["human_total"] += 1 
        confusion_matrix["ss_total"]["human_total"] += 1
    confusion_matrix["ss_total"]["human_total"] -= uncounted

    # #TODO: built for one question
    # confusion_matrix = {
    #     "human_democrat": {
    #         "ss_democrat": 0,
    #         "ss_republican": 0,
    #         "ss_other": 0,
    #         "human_total": 0 
    #     },
    #     "human_republican": {
    #         "ss_democrat": 0,
    #         "ss_republican": 0,
    #         "ss_other": 0,
    #         "human_total": 0
    #     },
    #     "human_other": {
    #         "ss_democrat": 0,
    #         "ss_republican": 0,
    #         "ss_other": 0,
    #         "human_total": 0
    #     },
    #     "ss_total": {
    #         "ss_democrat": 0,
    #         "ss_republican": 0,
    #         "ss_other": 0,
    #         "human_total": 0,

    #     }
    # }

    # uncounted = 0
    # for index, ss_row in ss_responses.iterrows():
    #     human_row = human_responses.loc[human_responses['responseID'] == ss_row["responseID"]]
    #     for question in survey_questions:
    #         colns = survey_questions[question]["colns"]
    #         if survey_questions[question]["type"] == "multiple-choice":
    #             if human_row.iloc[0][colns[0]] == 1: # Democrat
    #                 if ss_row[colns[0]] == 1:
    #                     confusion_matrix["human_democrat"]["ss_democrat"] += 1
    #                     confusion_matrix["ss_total"]["ss_democrat"] += 1
    #                 elif ss_row[colns[0]] == 2:
    #                     confusion_matrix["human_democrat"]["ss_republican"] += 1
    #                     confusion_matrix["ss_total"]["ss_republican"] += 1
    #                 elif ss_row[colns[0]] == 3:
    #                     confusion_matrix["human_democrat"]["ss_other"] += 1
    #                     confusion_matrix["ss_total"]["ss_other"] += 1
    #                 else:
    #                     print ("Invalid ss row")
    #                     print (ss_row)
    #                     continue
    #                 confusion_matrix["human_democrat"]["human_total"] += 1     
    #             elif human_row.iloc[0][colns[0]] == 2: # Republican
    #                 if ss_row[colns[0]] == 1:
    #                     confusion_matrix["human_republican"]["ss_democrat"] += 1
    #                     confusion_matrix["ss_total"]["ss_democrat"] += 1
    #                 elif ss_row[colns[0]] == 2:
    #                     confusion_matrix["human_republican"]["ss_republican"] += 1                      
    #                     confusion_matrix["ss_total"]["ss_republican"] += 1
    #                 elif ss_row[colns[0]] == 3:
    #                     confusion_matrix["human_republican"]["ss_other"] += 1
    #                     confusion_matrix["ss_total"]["ss_other"] += 1
    #                 else:
    #                     print ("Invalid ss row")
    #                     print (ss_row)
    #                     continue
    #                 confusion_matrix["human_republican"]["human_total"] += 1                   
    #             elif human_row.iloc[0][colns[0]] == 3: # neither Democrat nor Republican (incl. 3d/minor party candidates and write-ins)
    #                 if ss_row[colns[0]] == 1:
    #                     confusion_matrix["human_other"]["ss_democrat"] += 1
    #                     confusion_matrix["ss_total"]["ss_democrat"] += 1
    #                 elif ss_row[colns[0]] == 2:
    #                     confusion_matrix["human_other"]["ss_republican"] += 1
    #                     confusion_matrix["ss_total"]["ss_republican"] += 1
    #                 elif ss_row[colns[0]] == 3:
    #                     confusion_matrix["human_other"]["ss_other"] += 1
    #                     confusion_matrix["ss_total"]["ss_other"] += 1
    #                 else:
    #                     print ("Invalid ss row")
    #                     print (ss_row)
    #                     continue
    #                 confusion_matrix["human_other"]["human_total"] += 1
    #             else:
    #                 if human_row.iloc[0][colns[0]] == 0:
    #                     uncounted += 1
    #                 else:
    #                     print("Invalid human row")
    #                     print(human_row)
    #                 continue
    #             confusion_matrix["ss_total"]["human_total"] += 1
    
    print ("Total invalid human responses:", uncounted)
    return pd.DataFrame.from_dict(confusion_matrix)

if __name__ == "__main__":

    print("Percent correct", evaluate())

    confusion_matrix = create_confusion_matrix(8)
    print(confusion_matrix)


    


