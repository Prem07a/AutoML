data_cleaning_prompt = """
load the data from the given path and perform the following steps sequentially. Write the entire code for each step:

1. Remove NA Values:
   - For Categorical Columns (object/str dtype): 
     - Impute missing values with the mode of the column.
     - Apply label encoding or pandas dummies to convert these columns into numerical format.
   - For Numeric Columns:
     - Impute missing values with the median of the column.

2. Data Type Conversion:
   - Convert numeric columns to integer type if all values are whole numbers.
   - Convert columns with decimal values to float type.

3. Drop Columns:
   - Remove columns that have more than 20 unique values, as these columns cannot be effectively converted.

4. Save:
   - Save the cleaned data at the save path as original data path please dont use any other path or name use same name.

Ensure that all object/str types are converted to to correct type if not perform it again

"""

feature_selection_prompt = """

1. Remove Outliers:
   - Use the Interquartile Range (IQR) method to detect and remove outliers for numeric features.
    If after this step data is reduced by more than 10% cancel the operation and contine feature selection
2. Feature Selection:
    pvalue constant = 0.1
   - Apply statistical tests to select the best features based on p-values with target columns.
   - Keep the target column in the dataset; do not remove it.

3. Save:
   - Compulsary Save the dataset with selected features, including the target column, same path where original data was with same name.
"""

model_training_prompt = """
Train and evaluate machine learning models based on the target column in the dataset at '../train.csv'. Follow these steps:
Dont do any modification to data we have already done it you just train model on it

Import joblib compulsary to save model using: code: import joblib

1. Train the Model:
   - Split the dataset into training and testing sets.
   - Train various models appropriate for the target column's type (classification or regression).


2. Evaluate the Model:
   - For classification: Use metrics such as accuracy, precision, recall, and F1-score.
   - For regression: Use metrics such as RMSE, MAE, and R^2.
   - Perform cross-validation to ensure the model's generalization.
   - Save all the models at the path given aboe save_model_path

4. Save Performance Metrics:
   - Save the model performance metrics in JSON format to given path. name for json file: performance.json

5. Plot Performance:
   - Create a plot comparing the performance metrics of the different models.
   - Save the plot as performance.png in the given folder. dont use plt.show()
   
Compulsary do the saving of model, performance.json and performance.png
"""


