import pandas as pd
df = pd.read_excel('Amostra - GPS.xlsx', header=1)
print("\n".join(df.columns.tolist()))
