import pandas as pd
df = pd.read_csv('therapy_3.csv')


for i in range(3):
    df.iloc[i, 0] = df.iloc[i, 0] + "\n\n###\n\n"
    df.iloc[i, 1] = " " + df.iloc[i, 1] + "\n###\n"
    print(df.iloc[i, 0])
    
df.to_csv('therapy_3_a.csv', index=False)