age_mappings = {
    1: '18-29',
    2: '30-44',
    3: '45-59',
    4: '60+'
}

party_mappings = {
    -1: 'am unknown',
    1: 'am a strong Democrat',
    2: 'am a not so strong Democrat',
    3: 'am a lean Democrat',
    4: 'am a Independent',
    5: 'am a lean Republican',
    6: 'am a not so strong Republican',
    7: 'am a strong Republican'
}

ideology_mappings = {
    -1: 'unknown',
    1: 'very liberal',
    2: 'somewhat liberal',
    3: 'moderate',
    4: 'somewhat conservative',
    5: 'very conservative'
}

religion_mappings = {
    1: 'Protestant',
    2: 'Roman Catholic',
    3: 'Mormon',
    4: 'Orthodox',
    5: 'Jewish',
    6: 'Muslim',
    7: 'Buddhist',
    8: 'Hindu',
    9: 'Atheist',
    10: 'Agnostic',
    11: 'nothing in particular',
    12: 'Just Christian',
    13: 'Unitarian',
    14: 'something else',
    77: 'don\'t know',
    98: None
}

attend_mappings = {
    1: 'never',
    2: 'less than once per year',
    3: 'about once or twice per year',
    4: 'several times a year',
    5: 'about once a month',
    6: '2 or 3 times a month',
    7: 'nearly every week',
    8: 'every week',
    9: 'several times a week',
    77: 'don\'t know',
    98: None
}

race_mappings = {
    1: 'White, non-Hispanic',
    2: 'Black, non-Hispanic',
    3: 'Other, non-Hispanic',
    4: 'Hispanic',
    5: '2+, non-Hispanic',
    6: 'Asian, non-Hispanic'
}

marital_mappings = {
    1: 'married',
    2: 'widowed',
    3: 'divorced',
    4: 'separated',
    5: 'never married',
    6: 'living with partner'
}

employ_mappings = {
    1: 'working (as a paid employee)',
    2: 'working (self-employed)',
    3: 'not working (on temporary layoff from a job)',
    4: 'not working (looking for work)',
    5: 'not working (retired)',
    6: 'not working (disabled)',
    7: 'not working (other)'
}

income_mappings = {
    1: 'Less than $30,000',
    2: '$30,000 to under $60,000',
    3: '$60,000 to under $100,000',
    4: '$100,000 or more',
    77: 'don\'t known',
    99: 'refused to answer'
}

state_mappings = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

internet_mappings = {
    0: 'non-Internet',
    1: 'Internet'
}


def mapping_question_order(value):
    if 1 <= value <= 3:
        return 3
    elif 4 <= value <= 6:
        return 4
    elif 7 <= value <= 9:
        return 5
    else:
        return 6


def get_question(order_value, treatment):
    questions = {
        3: f'How much of this difference is mainly due to discrimination toward {treatment}?',
        4: f'How much of this difference is because most {treatment} have less in-born ability to learn?',
        5: (f'How much of this difference is because most {treatment} don\'t have the chance for education '
            f'that it takes to rise out of poverty?'),
        6: (f'How much of this difference is because most {treatment} just don\'t have the motivation '
            f'or will power to pull themselves out of poverty?')
    }
    return questions[order_value]


def generate_message(row):
    p_cond = int(row['P_COND'])
    if p_cond == 1:
        treatment = 'Blacks'
        w = 'Whites'
    elif p_cond == 2:
        treatment = 'Black men'
        w = 'White men'
    else:
        treatment = 'Black women'
        w = 'White women'

    o1 = mapping_question_order(row['ORDER1'])
    o2 = mapping_question_order(row['ORDER2'])
    o3 = mapping_question_order(row['ORDER3'])
    o4 = mapping_question_order(row['ORDER4'])
    order1 = get_question(o1, treatment)
    order2 = get_question(o2, treatment)
    order3 = get_question(o3, treatment)
    order4 = get_question(o4, treatment)

    ask = ('Choose the answer for each question from: 1. A great deal; 2. Some; 3. A little; 4. None. '
           'Please reply only with the number.')

    question = (f'Q1: {order1} '
                f'Q2: {order2} '
                f'Q3: {order3} '
                f'Q4: {order4} '
                f'{ask} ')

    display = (f'According to the following background, please answer four questions. '
               f'In the United States, {treatment} are much more likely to be unemployed than are {w}. '
               f'The unemployment rate is defined as the percentage of jobless people who have actively sought work '
               f'in the previous four weeks. According to the U.S. Bureau of Labor Statistics, '
               f'the average unemployment rate for {treatment} in 2016 was about 2 times higher than '
               f'the unemployment rate for {w}. ')

    answer1 = int(row[f'Q{o1}_{p_cond}'])
    answer2 = int(row[f'Q{o2}_{p_cond}'])
    answer3 = int(row[f'Q{o3}_{p_cond}'])
    answer4 = int(row[f'Q{o4}_{p_cond}'])
    answer = (f'Q1: {answer1}; '
              f'Q2: {answer2}; '
              f'Q3: {answer3}; '
              f'Q4: {answer4}; ')

    party_id = party_mappings[int(row['PartyID7'])]
    party_background = f'Politically, I {party_id}. '

    ideology = ideology_mappings[int(row['IDEO'])]
    ideology_background = f'Ideologically, I am {ideology}. '

    religion = religion_mappings[int(row['RELIG'])]
    if religion:
        if religion == 'something else':
            religion = row['RELIG_OE']
        religion_background = f'My religion is {religion}. '
    else:
        religion_background = ''

    attend = attend_mappings[int(row['ATTEND'])]
    if attend:
        attend_background = f'The frequency I attend religious services is {attend}. '
    else:
        attend_background = ''

    lang = 'English' if int(row['SURV_LANG']) == 1 else 'Spanish'
    lang_background = f'Survey Interview Language is {lang}. '

    if int(row['GENDER']) == 0:
        gender = 'unknown'
    elif int(row['GENDER']) == 1:
        gender = 'Male'
    else:
        gender = 'Female'
    gender_background = f'My gender is {gender}. '

    age = age_mappings[int(row['AGE4'])]
    age_background = f'In terms of my age, I am {age}. '

    race = race_mappings[int(row['RACETHNICITY'])]
    race_background = f'In terms of my race, I am {race}. '

    marital = marital_mappings[int(row['MARITAL'])]
    marital_background = f'In terms of my marital status, I am {marital}. '

    employ = employ_mappings[int(row['EMPLOY'])]
    employ_background = f'In terms of my employment status, I am {employ}. '

    income = income_mappings[int(row['INCOME4'])]
    income_background = f'My income is {income}. '

    state = state_mappings[row['STATE']]
    state_background = f'I live in {state}. '

    internet = internet_mappings[int(row['INTERNET'])]
    internet_background = f'My household has {internet}. '

    background_content = ('Pretend you are the following real person. Here is a description of this person: ' +
                          party_background +
                          ideology_background +
                          religion_background +
                          attend_background +
                          lang_background +
                          gender_background +
                          age_background +
                          race_background +
                          marital_background +
                          employ_background +
                          income_background +
                          state_background +
                          internet_background
                          )

    return background_content + display + question, answer
