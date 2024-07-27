
# Step 1: Remove NA Values

import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the data
data_path = '../project/Test/data/train_dataset.csv'
df = pd.read_csv(data_path)

# Impute missing values for categorical columns with mode and apply label encoding
for col in df.select_dtypes(include=['object']):
    df[col].fillna(df[col].mode()[0], inplace=True)
    df[col] = LabelEncoder().fit_transform(df[col])

# Impute missing values for numeric columns with median
for col in df.select_dtypes(include=['int64', 'float64']):
    df[col].fillna(df[col].median(), inplace=True)

# Step 2: Data Type Conversion

# Convert numeric columns to integer type if all values are whole numbers
for col in df.select_dtypes(include=['int64']):
    if (df[col] % 1 == 0).all():
        df[col] = df[col].astype(int)

# Convert columns with decimal values to float type
for col in df.select_dtypes(include=['float64']):
    df[col] = df[col].astype(float)

# Step 3: Drop Columns with more than 20 unique values
for col in df.columns:
    if df[col].nunique() > 20:
        df.drop(col, axis=1, inplace=True)

# Step 4: Save the cleaned data
df.to_csv(data_path, index=False)
