import os

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

class LogisticRegression:
    """Simple implementation of Logistic Regression with NumPy

    Attributes:
        weights (np.array): The model's weights,
        bias (float): The model's bias',
        threshold (float): Probability threshold for classification,
        learning_rate (float): Step size for gradient descent.

    """


    def __init__(self, n_inputs, bias=1.0, threshold=0.5, learning_rate=0.01):
        """Initialize the LogisticRegression model with random weights."""
        np.random.seed(42)
        self.weights = np.random.randn(n_inputs) * 0.01
        self.bias = bias
        self.threshold = threshold
        self.learning_rate = learning_rate

    def weighted_sum(self, X):
        """Compute the linear combination of inputs."""
        return np.dot(X, self.weights) + self.bias

    def sigmoid(self, z):
        """Apply the sigmoid activation function."""
        return 1 / (1 + np.exp(-z))

    def predict_proba(self, X):
        """Predict probabilities using the logistic function."""
        return self.sigmoid(self.weighted_sum(X))

    def predict_class(self, X):
        """
           Predict binary class (0 or 1) based on threshold.

           Returns:
               int: Predicted class label.
        """
        return int(self.predict_proba(X) >= self.threshold)

    def calc_loss(self, y_predicted, y_expected):
        """Compute binary cross-entropy loss."""
        y_predicted = np.clip(y_predicted, 1e-12, 1 - 1e-12)
        loss = -(y_expected * np.log(y_predicted) + (1 - y_expected) * np.log(1 - y_predicted))
        return np.mean(loss)

    def train(self, X, y, epochs=1000):
        """
            Train the model using gradient descent.

            Args:
                X (np.ndarray): Feature matrix.
                y (np.ndarray): Labels.
                epochs (int): Number of training iterations.
        """
        X = np.array(X)
        y = np.array(y)
        for epoch in range(epochs):
            y_pred = self.predict_proba(X)
            error = y_pred - y
            grad_w = np.dot(X.T, error) / len(y)
            grad_b = np.mean(error)
            self.weights -= self.learning_rate * grad_w
            self.bias -= self.learning_rate * grad_b
            if epoch % 100 == 0 or epoch == epochs - 1:
                loss = self.calc_loss(y_pred, y)
                print(f"Epoch {epoch}: Loss = {loss:.4f}")


def load_and_prepare_data():
    """
        Load and preprocess loan application data.

        Steps:
        - Load CSV data
        - Handle missing values
        - Encode categorical variables
        - Scale features

        Returns:
            tuple: (X_scaled, y, scaler, label_encoders, selected_features)
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    data_path = os.path.join(BASE_DIR, 'model_datasets', 'train.csv')
    # Load dataset
    df = pd.read_csv(data_path)

    #Drop rows where target label is missing
    df = df.dropna(subset=['Loan_Status'])

    # Fill missing values with statistical estimates
    df.fillna({
        'Gender': df['Gender'].mode()[0],
        'Married': df['Married'].mode()[0],
        'Dependents': df['Dependents'].mode()[0],
        'Self_Employed': df['Self_Employed'].mode()[0],
        'LoanAmount': df['LoanAmount'].median(),
        'Loan_Amount_Term': df['Loan_Amount_Term'].mode()[0],
        'Credit_History': df['Credit_History'].mode()[0],
    }, inplace=True)

    # Encode categorical columns
    categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    # Select features and target
    features = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
                'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term',
                'Credit_History', 'Property_Area']
    selected_features = features
    X = df[features].values
    y = df['Loan_Status'].map({'Y': 1, 'N': 0}).values

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, label_encoders, selected_features

def train_and_evaluate_model():
    """
        Train logistic regression model and evaluate its performance.

        Returns:
            tuple: (model, scaler, label_encoders, selected_features, accuracy)
    """

    # Load and preprocess data
    X, y, scaler, label_encoders, selected_features = load_and_prepare_data()

    # Split data into train/test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Train the model
    model = LogisticRegression(n_inputs=X_train.shape[1], learning_rate=0.01, threshold=0.4)
    model.train(X_train, y_train, epochs=2000)

    y_pred = [model.predict_class(x) for x in X_test]
    accuracy = round(accuracy_score(y_test, y_pred),2) * 100

    # Calculate evaluation metrics
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.2f}")
    print(f"Precision: {precision_score(y_test, y_pred):.2f}")
    print(f"Recall   : {recall_score(y_test, y_pred):.2f}")
    print(f"F1 Score : {f1_score(y_test, y_pred):.2f}")
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    return model, scaler, label_encoders, selected_features, accuracy

