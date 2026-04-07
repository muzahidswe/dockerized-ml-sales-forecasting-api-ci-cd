import pandas as pd
import pickle
import os
from sklearn.linear_model import LinearRegression


# create output folder
os.makedirs("models/outlet", exist_ok=True)

# load data
df = pd.read_excel("sample_data/retailer_sales.xlsx")

# function: time-series → supervised
# window = 12 || means analysis 12 months means whole years cycle
def create_dataset(series, window=12):
    X, y = [], []
    
    for i in range(len(series) - window):
        X.append(series[i:i+window])
        y.append(series[i+window])
        
    return X, y

global_X = []
global_y = []
all_retailer_data = {}

for i, row in df.iterrows():
    outlet_id = row['Retailer_Id']
    
    # 60 months sales
    sales = row.iloc[2:].values.astype(float)

    all_retailer_data[outlet_id] = sales.tolist()
    
    X, y = create_dataset(sales, window=12)
    
    # collect for global model
    global_X.extend(X)
    global_y.extend(y)
    
    # train per outlet model
    model = LinearRegression()
    model.fit(X, y)
    
    # save model
    with open(f"models/outlet/model_{outlet_id}.pkl", "wb") as f:
        pickle.dump(model, f)

# train global model
global_model = LinearRegression()
global_model.fit(global_X, global_y)

with open("models/outlet/global_model.pkl", "wb") as f:
    pickle.dump(global_model, f)


# dictionary created. No need to search data from DB
with open("models/outlet/all_retailer_data.pkl", "wb") as f:
    pickle.dump(all_retailer_data, f)

print("✅ Training complete. Models and Data Dictionary saved in /models/retailer folder")