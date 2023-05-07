import pandas as pd
import joblib
import time

# Load the trained KNN model
knn = joblib.load('knn_model.pkl')

# Initialize the number of rows processed to 0
num_rows_processed = 0

# Initialize the result dataframe
result = pd.DataFrame(columns=['prediction'])

while True:
    # Load the CSV file using pandas
    df = pd.read_csv('flows.csv')

    # Extract the new rows that have been added since the last prediction
    df_new = df.iloc[num_rows_processed:]

    if len(df_new) > 0:
        # Extract the required 7 features
        features = [
            "bwd_pkt_len_std",
            "flow_byts_s",
            "totlen_fwd_pkts",
            "fwd_pkt_len_std",
            "flow_iat_std",
            "flow_iat_min",
            "fwd_iat_tot"
        ]
        X_new = df_new[features].values
        y_pred = knn.predict(X_new)
        result = result.append(pd.DataFrame(y_pred, columns=['prediction']))
        rows_with_pred = result.loc[result['prediction'] == 1].index
        columns_to_extract = ['timestamp', 'src_ip',
                              'dst_ip', 'src_port', 'dst_port', 'protocol']
        fin_data = df_new.loc[rows_with_pred, columns_to_extract]
        num_rows_processed += len(df_new)
    time.sleep(300)
