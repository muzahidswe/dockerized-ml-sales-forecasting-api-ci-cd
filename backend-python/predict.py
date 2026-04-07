import pickle
import numpy as np
import pandas as pd
import os
from fastapi import FastAPI
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = FastAPI()

# 1. Function for Model Load
def load_model(outlet_id):
    model_path = f"models/outlet/model_{outlet_id}.pkl"
    global_model_path = "models/outlet/global_model.pkl"
    
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f), "Individual Model"
    else:
        with open(global_model_path, "rb") as f:
            return pickle.load(f), "Global Model"

# # 2. Main Prediction Logic
# def run_prediction():
#     # check parameter id exist or not
#     if len(sys.argv) < 2:
#         print("❌ Error: Please provide an Outlet ID. Example: python3 predict.py 1001")
#         return

#     outlet_id = sys.argv[1]
    
#     # 3. Finding last 12 months sales data from excel 
#     try:
#         # df = pd.read_excel("../sample_data/retailer_sales.xlsx") # dont need to read full excel file
#         # # Retailer_Id from excel file
#         # row = df[df['Retailer_Id'].astype(str) == str(outlet_id)]

#         with open("../models/outlet/all_retailer_data.pkl", "rb") as f: # dont need to read full excel file thats why create dictionary 
#             all_retailer_data = pickle.load(f)
        
#         if int(outlet_id) not in all_retailer_data:
#             print(f"❌ Error: Outlet ID {outlet_id} not found in Excel.")
#             return
            
#         # # Getting last 12 months sales data
#         # last_12_months = row.iloc[:, -12:].values.flatten().tolist()
#         history = all_retailer_data.get(int(outlet_id), [])

#         if len(history) < 12:
#             print(f"⚠️ Warning: Outlet {outlet_id} only has {len(history)} months of data. Need at least 12.")
#             return
#         last_12_months = history[-12:]
        
#         # 4. Model load and 12 month's prediction
#         model, model_type = load_model(outlet_id)
#         current_window = list(last_12_months)
#         predictions = []

#         for _ in range(12):
#             input_data = np.array(current_window).reshape(1, -1)
#             next_val = model.predict(input_data)[0]
#             predictions.append(max(0, next_val)) # Sales can't be negative
            
#             current_window.pop(0)
#             current_window.append(next_val)

#         # 5. Result
#         start_date = datetime.now().replace(day=1) + relativedelta(months=1)

#         for i, val in enumerate(predictions, 1):
            
#             prediction_month = start_date + relativedelta(months=i)
            
#             month_name = prediction_month.strftime("%b-%y")
#             print(f"{month_name}: {round(val, 2)}")

#     except Exception as e:
#         print(f"❌ An error occurred: {e}")

# # for script checking
# if __name__ == "__main__":
#     run_prediction()


# for fast api 
@app.get("/predict/{outlet_id}")
async def get_prediction(outlet_id: str):
    try:
        # Load the pre-processed retailer data dictionary
        # This is faster than reading the entire Excel file every time
        with open("models/outlet/all_retailer_data.pkl", "rb") as f:
            all_retailer_data = pickle.load(f)
        
        # Convert incoming string ID to integer to match dictionary keys
        target_id = int(outlet_id)
        
        if target_id not in all_retailer_data:
            return {
                'status' : False,
                'message': f"Outlet ID {outlet_id} not found in database.",
                'data': {}
            }
            
        # Get sales history (list of monthly sales)
        history = all_retailer_data.get(target_id, [])

        # Validate if we have enough data (minimum 12 months required for the window)
        if len(history) < 12:
            return {
                'status' : False,
                'message': f"Outlet {outlet_id} only has {len(history)} months of data. Minimum 12 months required.",
                'data': {}
            }
            
        # Use the most recent 12 months as the starting window
        last_12_months = history[-12:]
        
        # Load the appropriate model
        model, model_type = load_model(outlet_id)
        current_window = list(last_12_months)
        predictions_output = {}

        # Set the starting prediction month (e.g., next month from today)
        start_date = datetime.now().replace(day=1) + relativedelta(months=1)

        # 3. Recursive Prediction Loop (12 Months)
        for i in range(12):
            # Reshape data for model input: [1, 12]
            input_data = np.array(current_window).reshape(1, -1)
            
            # Predict next value and convert NumPy float to Python float for JSON compatibility
            raw_prediction = model.predict(input_data)[0]
            next_val = float(raw_prediction)
            
            # Ensure sales are not negative
            final_val = max(0, next_val)
            
            # Calculate the specific month name (e.g., Mar-26)
            prediction_month = start_date + relativedelta(months=i)
            month_label = prediction_month.strftime("%b-%y")
            
            # Store result
            predictions_output[month_label] = round(final_val, 2)
            
            # Slide the window: remove oldest, add newest predicted value
            current_window.pop(0)
            current_window.append(next_val)

        # 4. Return Final JSON Response
        return {
            'status' : True,
            'message': 'Prediction Found Successfully.',
            'data': {
                outlet_id : predictions_output
            }
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)