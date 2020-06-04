import numpy as np
import xgboost as xgb

# Instantiate Federated XGBoost
fed = xgb.Federated()

# Get number of federating parties
print(fed.get_num_parties())

# Load training data
# Ensure that each party's data is in the same location with the same name
dtrain = fed.load_data("../data/hb_train.csv")
dval = fed.load_data("../data/hb_val.csv")

# Train a model
params = {
        "max_depth": 3, 
        "min_child_weight": 1.0, 
        "lambda": 1.0,
        "tree_method": "hist",
        "objective": "binary:logistic"
        }

num_rounds = 20
bst = xgb.train(params, dtrain, num_rounds, evals=[(dtrain, "dtrain"), (dval, "dval")])

dtest = fed.load_data("../data/hb_test.csv")

# Get predictions
ypred = bst.predict(dtest)

print("The first twenty predictions are: ", ypred[:20])

# Save the model
bst.save_model("sample_model.model")

# Shutdown
fed.shutdown()


