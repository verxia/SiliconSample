from openai import OpenAI

import sys
sys.path.append("./")
from api_key import API_KEY

def lc( t ):
    return t.lower()

def uc( t ):
    return t.upper()

def mc( t ):
    tmp = t.lower()
    return tmp[0].upper() + t[1:]

client = OpenAI(api_key=API_KEY)
import numpy as np
import time

def gen_variants( toks ):
    results = []
    variants = [ lc, uc, mc ]
    for t in toks:
        for v in variants:
            results.append( " " + v(t) )
    return results


def do_query( prompt, max_tokens=2, model="gpt-3.5-turbo" ):

    response = client.chat.completions.create(
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=1,
        logprobs=True,
        top_logprobs=1
    )

    token_responses = response.choices[0].logprobs.content[0].top_logprobs
    results = {}

    for i, logprob in enumerate(token_responses):
        results[logprob.token] = np.round(np.exp(logprob.logprob)*100,2)

    print ("RESULTS")
    print(results)

    return results, response
    
def run_prompts( prompts, tok_sets ):
    results = []
    for prompt in prompts:
        # print("---------------------------------------------------")
        # print( prompt )
        response, full_response = do_query( prompt, max_tokens = 2 )
        # print( response )
        # print_response( prompt, tok_sets, response )
        time.sleep( 0.1 )
    return results

