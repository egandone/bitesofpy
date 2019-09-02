import pandas as pd
from collections import Counter

data = "http://projects.bobbelderbos.com/data/summer.csv"

def athletes_most_medals():
    summer = pd.read_csv(data)
    name_counter = Counter(summer.Athlete)
    return {t[0]:t[1] for t in name_counter.most_common(2)}
