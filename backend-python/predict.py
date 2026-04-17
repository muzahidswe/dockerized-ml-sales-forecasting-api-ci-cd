import pickle
import numpy as np
import os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

def load_model(outlet_id):
    model_path = f"models/outlet/model_{outlet_id}.pkl"
    global_model_path = "models/outlet/global_model.pkl"
    
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f), "Individual Model"
    else:
        with open(global_model_path, "rb") as f:
            return pickle.load(f), "Global Model"

def handler(event, context):
    try:

        outlet_id = event.get('outlet_id') or event.get('pathParameters', {}).get('outlet_id')

        if not outlet_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Outlet ID is required'})
            }

        
        with open("models/outlet/all_retailer_data.pkl", "rb") as f:
            all_retailer_data = pickle.load(f)
        
        target_id = int(outlet_id)
        
        if target_id not in all_retailer_data:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': f"Outlet ID {outlet_id} not found."})
            }
            
        history = all_retailer_data.get(target_id, [])

        if len(history) < 12:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': f"Insufficient data for outlet {outlet_id}"})
            }
            
        last_12_months = history[-12:]
        model, model_type = load_model(outlet_id)
        current_window = list(last_12_months)
        predictions_output = {}

        start_date = datetime.now().replace(day=1) + relativedelta(months=1)

        for i in range(12):
            input_data = np.array(current_window).reshape(1, -1)
            raw_prediction = model.predict(input_data)[0]
            next_val = float(raw_prediction)
            final_val = max(0, next_val)
            
            prediction_month = start_date + relativedelta(months=i)
            month_label = prediction_month.strftime("%b-%y")
            
            predictions_output[month_label] = round(final_val, 2)
            
            current_window.pop(0)
            current_window.append(next_val)

        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': True,
                'model_used': model_type,
                'data': { outlet_id: predictions_output }
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }