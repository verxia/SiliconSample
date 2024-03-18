import pandas as pd
import json
import ANES_all.editedSurvey.choice_mappings as anes_all
import ANES_argyle.editedSurvey.choice_mappings as anes_argyle
import CSEE.editedSurvey.choice_mappings as csee
from file_paths import *

#TODO: if missing some demographic info

# For a given response
def construct_persona_csee(row):
    p_gender = "You identify as " + csee.gender_mapping[row["gender"]] + ". "
    p_prov = "You live in " + csee.prov_mapping[row["prov"]] + ", Canada. "
    p_age_born = "You were born in " + csee.age_born_mapping[int(row["age_born"])] + ". " if (row["age_born"] != ".") else ""
    p_tongue = "The language you use most often in your household is " + csee.tongue_mapping[row["tongue"]] + ". " if (row["tongue"] != 98) else ""
    p_parent = "You " + csee.parent_mapping[row["parent"]] + ". "
    p_ev = csee.ev_mapping[int(row["ev"])] if (row["ev"] != "." and int(row["ev"]) != 97 and int(row["ev"]) != 98) else ""

    p_media = []
    for i in range(1,6):
        if row["media_" + str(i)] == "1":
            p_media.append(csee.media_mapping[i])
    p_media = "The media you consume most in your daily life is " + ", ".join(p_media) + ". "

    p_eth = []
    for i in range(1, 7):
        if row["eth_" + str(i)] == "1":
            p_eth.append(csee.eth_mapping[i])
    if row["eth_7"] == 1:
        p_eth.append(row["eth_8"])
    p_eth = "You identify as " + ", ".join(p_eth) + ". "

    if row["ideology"] == 98:
        p_ideology = ""
    else:
        p_ideology = "Generally speaking, you consider yourself on the " + csee.ideology_mapping[row["ideology"]] + " side of the political spectrum. "
    p_fed_vote = "If the federal elections were held today, you would vote for " + csee.fed_vote_mapping[row["fed_vote"]] + ". "
    p_educ = "The highest level of education you have attained is " + csee.educ_mapping[row["educ"]] + ". "
    p_income = csee.income_mapping[row["income"]] + " best describes your gross family household income last year."

    return p_gender + p_prov + p_age_born + p_tongue + p_parent + p_ev + p_media + p_eth + p_ideology + p_fed_vote + p_educ + p_income

def construct_persona_anes_all(row):
    age = "You are " + anes_all.age_mapping[row["VCF0101"]] + " years old. " if anes_all.age_mapping[row["VCF0101"]] != "" else ""
    gender = "You identify as " + anes_all.gender_mapping[row["VCF0104"]] + ". " if anes_all.gender_mapping[row["VCF0104"]] != "" else ""
    race = "The racial or ethnic group or groups best describes you is " + anes_all.race_mapping[row["VCF0105a"]] + ". " if anes_all.race_mapping[row["VCF0105a"]] != "" else ""
    # urbanism = "You live in " + urbanism_mapping[row["VCF0111"]] + ". " if urbanism_mapping[row["VCF0111"]] != "" else ""
    income = "Your income is in the " + anes_all.income_mapping[row["VCF0114"]] + ". " if anes_all.income_mapping[row["VCF0114"]] != "" else ""
    union = anes_all.union_mapping[row["VCF0127"]]
    religion = "Your religion is " + anes_all.religion_mapping[row["VCF0128"]] + ". " if anes_all.religion_mapping[row["VCF0128"]] != "" else ""
    church = "You go to church " + anes_all.church_mapping[row["VCF0130"]] + ". " if anes_all.church_mapping[row["VCF0130"]] != "" else ""
    educ = "The highest level of education you've earned is " + anes_all.educ_mapping[row["VCF0140"]] + ". " if anes_all.educ_mapping[row["VCF0140"]] != "" else ""
    parents_born = anes_all.parents_born_mapping[row["VCF0143"]]
    home_ownership = anes_all.home_ownership_mapping[row["VCF0146"]]
    marital = anes_all.marital_mapping[row["VCF0147"]]
    postal = "You live in " + row["VCF0901b"] + " state. " if row["VCF0901b"] != 99 else ""
    # initial_party = "Generally thinking, you think of yourself as " + initial_party_mapping[row["VCF0302"]] + ". " if initial_party_mapping[row["VCF0302"]] != "" else ""
    interest = "You are " + anes_all.interest_mapping[row["VCF0310"]] + " in the political campaigns this year. " if anes_all.interest_mapping[row["VCF0310"]] != "" else ""
    # vote = "You voted " + vote_mapping[row["VCF0705"]] + ". " if vote_mapping[row["VCF0705"]] != "" else ""
    discuss = "You spent " + anes_all.discuss_mapping[row["VCF0733"]] + " in the past week talking about politics with family or friends. " if anes_all.discuss_mapping[row["VCF0733"]] != "" else ""
    lib_cons = "You identify as " + anes_all.lib_cons_mapping[row["VCF0849"]] + ". " if anes_all.lib_cons_mapping[row["VCF0849"]] != "" else ""

    return age + gender + race + income + union + religion + church + educ + parents_born + home_ownership + marital + postal + interest + discuss + lib_cons

def construct_persona_anes_argyle(row):
    age = "In terms of my age, I am " + str(row["VCF0101"]) + " years old. " if row["VCF0101"] != 0 else ""
    gender = "I am a " + anes_argyle.gender_mapping[row["VCF0104"]] + ". " if anes_argyle.gender_mapping[row["VCF0104"]] != "" else ""
    race = "Racially, I am " + anes_argyle.race_mapping[row["VCF0105a"]] + ". " if anes_argyle.race_mapping[row["VCF0105a"]] != "" else ""
    postal = "I live in " + row["VCF0901b"] + " state. " if row["VCF0901b"] != 99 else ""
    church = "I attend church " + anes_argyle.church_mapping[row["VCF0130"]] + ". " if anes_argyle.church_mapping[row["VCF0130"]] != "" else ""
    interest = "I am " + anes_argyle.interest_mapping[row["VCF0310"]] + " in the political campaigns this year. " if anes_argyle.interest_mapping[row["VCF0310"]] != "" else ""
    discuss = "I spent " + anes_argyle.discuss_mapping[row["VCF0733"]] + " in the past week talking about politics with family or friends. " if anes_argyle.discuss_mapping[row["VCF0733"]] != "" else ""
    partisanship = "I am a " + anes_argyle.partisanship[row["VCF0305"]] + ". " if anes_argyle.partisanship[row["VCF0305"]] != "" else ""
    lib_cons = "Ideologically, I describe myself as " + anes_argyle.lib_cons_mapping[row["VCF0803"]] + ". " if anes_argyle.lib_cons_mapping[row["VCF0803"]] != "" else ""
    initial_party = "Politically, I am a " + anes_argyle.initial_party_mapping[row["VCF0302"]] + ". " if anes_argyle.initial_party_mapping[row["VCF0302"]] != "" else ""


    return age + gender + race + postal + church + interest + discuss + partisanship + lib_cons + initial_party

def construct_personas():
    responses = pd.read_csv(RESPONSES_PATH)

    personas = {}
    for index, row in responses.iterrows():
        personas[row['responseID']] = construct_persona_anes_argyle(row)
    return personas

if __name__ == "__main__":
    personas = construct_personas()

    with open(PERSONAS_PATH, 'w') as fp:
        json.dump(personas, fp, indent=4)
