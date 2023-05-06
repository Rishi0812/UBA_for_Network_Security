import pandas as pd
import numpy as np
import joblib

# Load the trained KNN model
knn = joblib.load('knn_model.pkl')

# Load the CSV file using pandas
df = pd.read_csv('flows.csv')

# Extract the required 7 features
features = [
    "bwd_pkt_len_std",
"flow_byts_s",
"totlen_fwd_pkts",
"fwd_pkt_len_std"
"flow_iat_std",
"flow_iat_min",
"fwd_iat_tot"
]
X = df[features].values



# Make predictions using the trained KNN model
y_pred = knn.predict(X)

# Print the predictions
print(y_pred)
