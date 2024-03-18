import json
import os.path
import pyreadstat
from tqdm import tqdm
import support_functions as sf
SURVEY_INDEX = 1
SURVEY_PATH = ('/Users/chiyuwei/PycharmProjects/LLM_poli/data/surveys/1. Do White Americans’ Beliefs about Racial '
               'Inequality depend on the Sex of the Target Group? Evidence from a Survey Based Experiment')
DATA_NAME = 'TESS100_Behrends_client.dta'


def generate_json(df, name):
    message_list = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        instruction, answer = sf.generate_message(row)
        data = {'instruction': instruction,
                'input': "",
                'output': answer}
        message_list.append(data)
    with open(os.path.join(SURVEY_PATH, f'{name}.json'), 'w') as f:
        json.dump(message_list, f)


if __name__ == '__main__':
    df, meta = pyreadstat.read_dta(os.path.join(SURVEY_PATH, DATA_NAME))
    test = df.sample(frac=0.20, random_state=42)
    train = df.drop(test.index)
    generate_json(train, f'{SURVEY_INDEX}_train')
    generate_json(test, f'{SURVEY_INDEX}_test')
