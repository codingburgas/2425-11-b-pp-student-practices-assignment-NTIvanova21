import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from imblearn.over_sampling import SMOTE


class LogisticRegression:
    def __init__(self, n_inputs, bias=0.0, learning_rate=0.01, epochs=100, threshold=0.5):
        np.random.seed(42)
        self.n_inputs = n_inputs
        self.weights = np.random.rand(n_inputs)
        self.bias = bias
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.threshold = threshold

    def weighted_sum(self, X):
        X = np.array(X)
        if len(X) != self.n_inputs:
            raise ValueError("X and n_inputs must have the same length")
        return self.weights.dot(X) + self.bias

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def predict_probability(self, X):
        z = self.weighted_sum(X)
        return self.sigmoid(z)

    def predict_class(self, X):
        return int(self.predict_probability(X) >= self.threshold)

    def train(self, X, y):
        X = np.array(X)
        y = np.array(y)

        # Calculate class weights more effectively
        class_counts = np.bincount(y)
        n_samples = len(y)
        n_classes = len(class_counts)
        weights = n_samples / (n_classes * class_counts)

        for epoch in range(self.epochs):
            for inputs, y_expected in zip(X, y):
                y_predicted = self.predict_probability(inputs)
                y_predicted = np.clip(y_predicted, 1e-10, 1 - 1e-10)
                error = y_predicted - y_expected


                weight = weights[y_expected]
                self.weights -= self.learning_rate * error * np.array(inputs) * weight
                self.bias -= self.learning_rate * error * weight



df = pd.read_csv("AI_model/model_datasets/train.csv")

# Fill missing values
df.fillna({
    'Gender': df['Gender'].mode()[0],
    'Married': df['Married'].mode()[0],
    'Dependents': df['Dependents'].mode()[0],
    'Self_Employed': df['Self_Employed'].mode()[0],
    'LoanAmount': df['LoanAmount'].median(),
    'Loan_Amount_Term': df['Loan_Amount_Term'].mode()[0],
    'Credit_History': df['Credit_History'].mode()[0],
}, inplace=True)

categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le



features = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
            'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term',
            'Credit_History', 'Property_Area']


X = df[features].values
y = df['Loan_Status'].map({'Y': 1, 'N': 0}).values

selector = SelectKBest(score_func=f_classif, k=7)
X_selected = selector.fit_transform(X, y)
selected_features = [features[i] for i in selector.get_support(indices=True)]
print("Selected features:", selected_features)


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_selected)


smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)


X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, stratify=y_resampled,random_state=42)


model = LogisticRegression(n_inputs=X_train.shape[1], learning_rate=0.001, epochs=2000, threshold=0.5)
model.train(X_train, y_train)


y_pred = [model.predict_class(x) for x in X_test]
y_pred = np.array(y_pred)


accuracy = accuracy_score(y_test, y_pred)
accuracy = round(accuracy, 2) * 100
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)


print(f"\nEvaluation on Test Set:")
print(f"Accuracy     : {accuracy:.2f}")
print(f"Precision    : {precision:.2f}")
print(f"Recall       : {recall:.2f}")
print(f"F1 Score     : {f1:.2f}")
print("\nConfusion Matrix:")
print(conf_matrix)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))