import pandas as pd

df = pd.read_pickle('df_translation.pkl')

print(df.tail(50))