# The init and run functions will load and score the input using the saved model.
# The score.py file will be included in the web service deployment package.
def init():
    from sklearn.externals import joblib
    import pickle
    import os
    global model
    
    model_dir = "./models/dtree.pkl"
    model = joblib.load(model_dir)
#     model_dir = "C:/Users/nelgoh/Desktop/Resources/Petronas/energy_demand_forecast/EnergyDemandForecast/models/"
#     with open(os.path.join(model_dir, model_name + '.pkl'), 'rb') as f:
#         model = pickle.load(f)
#     with open('model_deploy.pkl', 'rb') as f:
#         model = pickle.load(f)
    
def run(input_df):
    input_df = input_df[['precip', 'temp', 'hour', 'month', 'dayofweek',
        'temp_lag1', 'temp_lag2', 'temp_lag3', 'temp_lag4', 'temp_lag5',
        'temp_lag6', 'demand_lag1', 'demand_lag2', 'demand_lag3',
        'demand_lag4', 'demand_lag5', 'demand_lag6']]
    try:
        if (input_df.shape != (1,17)):
            return 'Bad imput: Expecting dataframe of shape (1,17)'
        else:
            pred = model.predict(input_df)
            return int(pred)
    except Exception as e:
        return(str(e))