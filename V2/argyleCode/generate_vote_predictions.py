import sys
import pandas as pd
import pickle
from tqdm import tqdm

# for cost analysis
from transformers import GPT2Tokenizer

# if sys.argv[1] == '2012':
#     from anes2012 import *
# if sys.argv[1] == '2016':
#     from anes2016 import *
if sys.argv[1] == '2020':
    from anes2020 import *
from V2.common import *

foi_keys = fields_of_interest.keys()

#
# ============================================================================================
52
# ============================================================================================
#

def cost_approximation(prompt, engine="davinci", tokenizer=None):
    possible_engines = ["davinci", "curie", "babbage", "ada"]
    assert engine in possible_engines, f"{engine} is not a valid engine"

    if tokenizer==None:
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    num_tokens = len(tokenizer(prompt)['input_ids'])

    if engine == "davinci":
        cost = (num_tokens / 1000) * 0.0600
    elif engine == "curie":
        cost = (num_tokens / 1000) * 0.0060
    elif engine == "babbage":
        cost = (num_tokens / 1000) * 0.0012
    else:
        cost = (num_tokens / 1000) * 0.0008

    return cost, num_tokens

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

#
# ============================================================================================
# ============================================================================================
#

anesdf = pd.read_csv( ANES_FN, sep=SEP, encoding='latin-1' )

costs = []
numtoks = []
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

full_results = []

for pid in tqdm( range(len(anesdf)) ):

    if "V200003" in anesdf.iloc[pid] and anesdf.iloc[pid]["V200003"]==2:
        print( f"SKIPPING {pid}..." )
        # we want to exclude cases marked as 2 on this variable;
        # those are the panel respondents (interviewed in 2016 and 2020)
        continue

    anes_id = anesdf.iloc[pid][ID_COL]

    prompt = gen_backstory( pid, anesdf )
    prompt += " " + query

    #print("---------------------------------------------------")
    #print( prompt )

    cost, numtok = cost_approximation( prompt, engine="davinci", tokenizer=tokenizer )
    costs.append( cost )
    numtoks.append( numtok )    

    results = run_prompts( [prompt], tok_sets, engine="davinci" )
    #print(results[0][0])
    full_results.append( (anes_id, prompt, results) )

print( "Total cost: ", np.sum(np.array(costs)) )
print( "Averge numtok: ", np.mean(np.array(numtoks)) )
pickle.dump( full_results, open(OUTPUT_FN,"wb") )