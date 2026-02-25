import pandas as pd

try:
    df = pd.read_excel('Amostra - GPS.xlsx', header=None)
    print("Row 0 (potential noise):", df.iloc[0].values[:5])
    print("Row 1 (potential header):", df.iloc[1].values[:10])
    print("Row 2 (first data row):", df.iloc[2].values[:10])
    print("Last row:", df.iloc[-1].values[:5])
except Exception as e:
    print(f"Error: {e}")
