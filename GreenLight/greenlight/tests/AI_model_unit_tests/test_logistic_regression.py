import unittest
import numpy as np

from greenlight.AI_model.logistic_regression_model import LogisticRegression


class TestLogisticRegression(unittest.TestCase):
    """
       Unit tests for the custom LogisticRegression class.
    """
    def setUp(self):
        """
            Set up a logistic regression model with predefined weights and bias.
        """
        self.model = LogisticRegression(n_inputs = 3)
        self.model.weights = np.array([0.5, -0.6, 0.2])
        self.model.bias = 0.0
        self.model.threshold = 0.5

    def test_predict_class_positive(self):
        """
            Test that the model correctly predicts class 1 for a positive logit.
        """
        X = np.array([1.0, 0.0, 1.0])
        prediction = self.model.predict_class(X)
        self.assertEqual(prediction, 1)

    def test_predict_class_negative(self):
        """
            Test that the model correctly predicts class 0 for a negative logit.
        """
        X = np.array([0.0, 1.0, 0.0])
        prediction = self.model.predict_class(X)
        self.assertEqual(prediction, 0)

