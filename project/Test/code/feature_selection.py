
# Importing necessary libraries
import pandas as pd
import numpy as np
from scipy import stats

# Load the dataset
data_path = "../project/Test/data/train_dataset.csv"
df = pd.read_csv(data_path)

# Function to remove outliers using IQR method
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df

# Calculate initial number of rows
initial_rows = df.shape[0]

# Remove outliers for each numeric feature
numeric_columns = df.select_dtypes(include=[np.number]).columns
for column in numeric_columns:
    df = remove_outliers_iqr(df, column)

# Calculate percentage reduction in data
reduction_percent = ((initial_rows - df.shape[0]) / initial_rows) * 100

# If data reduced by more than 10%, cancel operation and continue with feature selection
if reduction_percent > 10:
    print("Data reduced by more than 10%. Cancelling outlier removal operation.")
else:
    # Feature selection based on p-values
    pvalue_constant = 0.1
    feature_columns = df.columns.drop('Survived')
    for feature in feature_columns:
        p_value = stats.ttest_ind(df[feature], df['Survived']).pvalue
        if p_value > pvalue_constant:
            df = df.drop(feature, axis=1)

    # Save the modified dataset with selected features
    save_path = "../project/Test/data/train_dataset.csv"
    df.to_csv(save_path, index=False)
    print("Dataset with selected features saved successfully at:", save_path)
