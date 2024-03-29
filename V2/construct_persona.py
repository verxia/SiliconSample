import pandas as pd
from choice_mapping import *

foi_keys = fields_of_interest.keys()

def gen_backstory( pid, df ):
    person = df.iloc[pid]

    backstory = ""

    for k in foi_keys:
        anes_val = person[k]
        elem_template = fields_of_interest[k]['template']
        elem_map = fields_of_interest[k]['valmap']

        if len(elem_map) == 0:
            backstory += " " + elem_template.replace( 'XXX', str(anes_val) )

        elif anes_val in elem_map:
            backstory += " " + elem_template.replace( 'XXX', elem_map[anes_val] )

    if backstory[0] == ' ':
        backstory = backstory[1:]

    return backstory

if __name__ == "__main__":
    pass
    # df = pd.read_csv("V2/2020_ANES.csv")
    # print(gen_backstory( 0, df ))
