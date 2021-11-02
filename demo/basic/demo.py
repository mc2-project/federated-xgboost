import sys
import federatedxgboost as fxgb 

# Federated XGBoost automatically runs your training script and passes it the rabit configuration as an argument
# All scripts must start with this line and pass `rabit_config` into xgb.Federated()
rabit_config = sys.argv[1]

# Instantiate Federated XGBoost
fed = fxgb.Federated(rabit_config)

# Get number of federating parties
print("Number of parties in federation: ", fed.get_num_parties())

# Load training data - pass in the absolute path to the data 
# Ensure that each party's data is in the same location with the same name
dtrain = fed.load_data("/home/opaque/federated-xgboost/demo/data/hb_train.csv")
dval = fed.load_data("/home/opaque/federated-xgboost/demo/data/hb_val.csv")

# Train a model
params = {
        "max_depth": 3, 
        "min_child_weight": 1.0, 
        "lambda": 1.0,
        "tree_method": "hist",
        "objective": "binary:logistic"
        }

num_rounds = 20
print("Training")
bst = fxgb.train(params, dtrain, num_rounds, evals=[(dtrain, "dtrain"), (dval, "dval")])

dtest = fed.load_data("/home/opaque/federated-xgboost/demo/data/hb_test.csv")

# Get predictions
print("Predicting")
ypred = bst.predict(dtest)

print("The first twenty predictions are: ", ypred[:20])

# Save the model
bst.save_model("sample_model.model")

# Shutdown
fed.shutdown()

