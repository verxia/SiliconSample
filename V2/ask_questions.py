import pandas as pd
from tqdm import tqdm
from construct_persona import *
from argyleCode.common import *

query = "In the 2020 presidential election, Donald Trump is the Republican candidate, "
query += "and Joe Biden is the Democratic candidate, and I voted for"

tok_sets = {
    "trump": gen_variants( [ "donald", "trump", "republican", "conservative" ] ),
    "biden": gen_variants( [ "joe", "joseph", "biden", "democrat", "democratic", "liberal"] ),
}
anesdf = pd.read_csv("V2/2020_ANES.csv")

full_results = []

for pid in tqdm( range(len(anesdf)) ):

    # TODO: Can't find what variable this is
    # if "V200003" in anesdf.iloc[pid] and anesdf.iloc[pid]["V200003"]==2:
    #     print( f"SKIPPING {pid}..." )
    #     # we want to exclude cases marked as 2 on this variable;
    #     # those are the panel respondents (interviewed in 2016 and 2020)
    #     continue

    anes_id = anesdf.iloc[pid]["responseID"]

    prompt = gen_backstory( pid, anesdf )
    prompt += " " + query

    #print("---------------------------------------------------")
    #print( prompt )

    # cost, numtok = cost_approximation( prompt, engine="davinci", tokenizer=tokenizer )
    # costs.append( cost )
    # numtoks.append( numtok )    

    results = run_prompts( [prompt], tok_sets, engine="davinci" )
    #print(results[0][0])
    full_results.append( (anes_id, prompt, results) )

# print( "Total cost: ", np.sum(np.array(costs)) )
# print( "Averge numtok: ", np.mean(np.array(numtoks)) )
    
print(full_results[:5])
