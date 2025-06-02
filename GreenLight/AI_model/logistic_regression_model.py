import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


class LogisticRegression:
    def __init__(self, n_inputs, bias=0.0, learning_rate=0.01, epochs=100, threshold=0.5):
        np.random.seed(43)
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

        if len(X) != len(y):
            raise ValueError("X and y must have the same length")

        for epoch in range(self.epochs):
            total_loss = 0

            for inputs, y_expected in zip(X, y):
                y_predicted = self.predict_probability(inputs)

                y_predicted = np.clip(y_predicted, 1e-10, 1 - 1e-10)

                loss = -(y_expected * np.log(y_predicted) + (1 - y_expected) * np.log(1 - y_predicted))
                total_loss += loss

                gradient = y_predicted - y_expected

                self.weights -= self.learning_rate * gradient * np.array(inputs)
                self.bias -= self.learning_rate * gradient


df = pd.read_csv("AI_model/model_datasets/train.csv")
df.fillna({
    'Gender': df['Gender'].mode()[0],
    'Married': df['Married'].mode()[0],
    'Dependents': df['Dependents'].mode()[0],
    'Self_Employed': df['Self_Employed'].mode()[0],
    'LoanAmount': df['LoanAmount'].median(),
    'Loan_Amount_Term': df['Loan_Amount_Term'].mode()[0],
    'Credit_History': df['Credit_History'].mode()[0],
}, inplace=True)


categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

features = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
            'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term'
            ]
X = df[features].values
y = df['Loan_Status'].map({'Y': 1, 'N': 0}).values


scaler = StandardScaler()
X = scaler.fit_transform(X)


model = LogisticRegression(n_inputs=X.shape[1], learning_rate=0.001, epochs=1000)
model.train(X, y)

y_pred = [model.predict_class(x) for x in X]
accuracy = np.mean(y_pred == y)
accuracy = round(accuracy, 2) * 100

print(f"Accuracy on the whole dataset: {accuracy}%")


