import unittest
import numpy as np
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AI_model.logistic_regression_model import LogisticRegression


class TestLogisticRegression(unittest.TestCase):
    def setUp(self):
        self.model = LogisticRegression(n_inputs = 3)
        self.model.weights = np.array([0.5, -0.6, 0.2])
        self.model.bias = 0.0
        self.model.threshold = 0.5

        def test_predict_class_positive(self):
            X = np.array([1.0, 0.0, 1.0])  # Weighted sum = 0.5 + 0.2 = 0.7 > 0.5
            prediction = self.model.predict_class(X)
            self.assertEqual(prediction, 1)

        def test_predict_class_negative(self):
            X = np.array([0.0, 1.0, 0.0])  # Weighted sum = -0.6 < 0.5
            prediction = self.model.predict_class(X)
            self.assertEqual(prediction, 0)

if __name__ == '__main__':
    unittest.main()