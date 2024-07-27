
import pandas as pd

# Load the data
data_path = "../project/Test/data/train_dataset.csv"
data = pd.read_csv(data_path)

# Drop Unnamed: 0 and Name columns
data.drop(['Unnamed: 0', 'Name'], axis=1, inplace=True)

# Save modified data to a new file
save_path = "../project/Test/data/temp.csv"
data.to_csv(save_path, index=False)
