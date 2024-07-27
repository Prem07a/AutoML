
# Importing necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
import joblib
import json
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('../project/Test/data/train_dataset.csv')

# Define features and target
X = data.drop('Survived', axis=1)
y = data['Survived']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize models
models = {
    'Logistic Regression': LogisticRegression(),
    'K-Nearest Neighbors Classification': KNeighborsClassifier(),
    'Support Vector Machine (SVM)': SVC(),
    'Decision Tree Classification': DecisionTreeClassifier(),
    'Random Forest Classification': RandomForestClassifier(),
    'Gradient Boosting Classification': GradientBoostingClassifier(),
    'AdaBoost Classification': AdaBoostClassifier()
}

# Train and evaluate models
model_metrics = {}
for model_name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    if 'Classification' in model_name:
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        model_metrics[model_name] = {'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1-score': f1}
    else:
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        r2 = r2_score(y_test, y_pred)
        
        model_metrics[model_name] = {'RMSE': rmse, 'R2': r2}

# Save models
save_model_path = '../project/Test/models/'
for model_name, model in models.items():
    joblib.dump(model, save_model_path + model_name + '.joblib')

# Save performance metrics
with open('../project/Test/report/performance.json', 'w') as f:
    json.dump(model_metrics, f)

# Plot performance metrics
metrics_df = pd.DataFrame(model_metrics).T
metrics_df.plot(kind='bar', figsize=(12, 6))
plt.xlabel('Models')
plt.ylabel('Metrics')
plt.title('Performance Metrics of Different Models')
plt.legend(title='Metrics')
plt.savefig('../project/Test/report/performance.png')
