import pandas as pd

def create_hand_histogram(raw_data: pd.DataFrame) -> pd.DataFrame:
    # Crib hands can have anywhere between 0 and 29 points
    crib_score_data = {
        'crib': [0 for i in range(30)],
        'not-crib': [0 for i in range(30)]
    }

    for _, row in raw_data.iterrows():
        if row['crib']:
            crib_score_data['crib'][row['score']] += 1
        else:
            crib_score_data['not-crib'][row['score']] += 1
    
    crib_score_data['total'] = [x + y for x,y in zip(crib_score_data['crib'], crib_score_data['not-crib'])]
    
    for section, data in (
        ('crib', raw_data[raw_data['crib'] == 1]),
        ('not-crib', raw_data[raw_data['crib'] == 0]),
        ('total', raw_data)
    ):
        crib_score_data[section].extend((data['score'].mean(), data['score'].std()))


    columns = [str(x) for x in range(30)] + ['mean', 'stddev']
    index = ['total', 'crib', 'not-crib']
    return pd.DataFrame(
        [crib_score_data[name] for name in index],
        columns=columns,
        index=index
    )
