fips_state_map = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

# Some keys changed to match complete ANES data coding
fields_of_interest = {
    # race 1= white 2= black 3 = asian 5 = hispanic
    'VCF0105a': {
        "template":"Racially, I am XXX.",
        "valmap":{ 1:'white', 2:'black', 3:'asian', 4:'native American', 5:'hispanic' },
    },

    # discuss_politics 1=yes discuss politics, 2=never discuss politics
    'VCF0731': {
        "template":"XXX",
        "valmap":{
        1:'I like to discuss politics with my family and friends.',
        2:'I never discuss politics with my family or friends.'},
    },

    # ideology 1-7 = extremely liberal, ..., extremely conservative
    'VCF0803': {
        "template":"Ideologically, I am XXX.",
        "valmap":{
        1:"extremely liberal",
        2:"liberal",
        3:"slightly liberal",
        4:"moderate",
        5:"slightly conservative",
        6:"conservative",
        7:"extremely conservative"},
        },

    # party
    'VCF0301': {
        "template":"Politically, I am XXX.",
        "valmap":{
        1:"a strong democrat",
        2:"a weak Democrat",
        3:"an independent who leans Democratic",
        4:"an independent",
        5:"an independent who leans Republican",
        6:"a weak Republican",
        7:"a strong Republican"},
    },

    # church_goer
    'VCF0130': {
        "template":"I XXX.",
        "valmap":{ 1:"attend church", 2:"do not attend church"},
    },

    # age
    'VCF0101': {
        "template":"I am XXX years old.",
        "valmap":{},
    },

    # gender 1=male 2=female
    'VCF0104': {
        "template":"I am a XXX.",
        "valmap":{ 1:"man", 2:"woman"},
    },
    # political_interest = if_else(V162256 > 0, V162256, NA_real_),
    'VCF0310': {
        "template":"I am XXX interested in politics.",
        "valmap":{1:"not very", 2:"somewhat", 3:"very much"},
    },
    
    # this is sample address, which may be different than registration address...?
    'VCF0901b': {
        "template":"I am from XXX.",
        "valmap":fips_state_map,
    },
}