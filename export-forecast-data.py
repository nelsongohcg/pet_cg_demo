import os
import pickle
import pandas as pd
from azure.storage.blob import BlockBlobService

block_blob_svc = BlockBlobService(account_name="petcgexperimentstorage", account_key="C+ffy45PBcicHAxWiRbW9MnFR651A8xbiVe2wkyZgolznhFf70caTZmpWIJb2spV5YFl/LQB0ARUfU+AQx6w9g==")
container_name = "energy-demand-demo/prediction-forecast-csv"

list_of_model_names = [
    "linear_regression", 
    "ridge", 
    "ridge_poly2",
    "mlp", 
    "dtree", 
    "gbm", 
    "xgboost"
]

min_date = '2016-07-01'
max_date = '2016-07-07'

for each_model_name in list_of_model_names:
    
    prediction_df_dir = "C:/Users/nelgoh/Desktop/Resources/Petronas/energy_demand_forecast/EnergyDemandForecast/outputs/prediction_dfs/"
    with open(os.path.join(prediction_df_dir, each_model_name + '_predictions.pkl'), 'rb') as f:
        predictions = pickle.load(f)

    for n in range(1, 7):    
        predictions['error_t+'+str(n)] = predictions['pred_t+'+str(n)] - predictions['demand']
        predictions['abs_error_t+'+str(n)] = abs(predictions['error_t+'+str(n)])
        predictions['abs_pct_error_t+'+str(n)] = abs(predictions['error_t+'+str(n)]) / predictions['demand']    

    # predictions.to_csv('./outputs/prediction_csv/' + each_model_name + '_prediction_forecast.csv')
    prediction_output = predictions.to_csv(encoding="utf-8")
    blob_name = each_model_name + '_prediction_forecast.csv'
    print("Exporting data to the Blob Storage...")
    block_blob_svc.create_blob_from_text(container_name, blob_name, prediction_output)

