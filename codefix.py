import pandas as pd

df = pd.DataFrame(columns=["Date", "Amount", "Category", "Description"])
df.to_csv("finance_data.csv", index=False)