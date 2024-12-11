# pip install unittest2

import unittest
import pandas as pd
from sklearn.datasets import make_regression
from pipeline import DataPreprocessor, ModelTrainer, Pipeline  # Asegúrate de que las clases estén en 'pipeline.py'

class TestDataPreprocessor(unittest.TestCase):
    def setUp(self):
        X, y = make_regression(n_samples=100, n_features=1, noise=0.1)
        self.df = pd.DataFrame({'Price': y})
        self.preprocessor = DataPreprocessor(lags=5, train_size=0.7)

    def test_create_lag_features(self):
        df_lag = self.preprocessor.create_lag_features(self.df)
        expected_columns = ['Price'] + [f'lag_{i}' for i in range(1, 6)]
        self.assertListEqual(list(df_lag.columns), expected_columns)
        self.assertEqual(len(df_lag), 100 - 5)

    def test_split_data(self):
        df_lag = self.preprocessor.create_lag_features(self.df)
        X_train, y_train, X_test, y_test = self.preprocessor.split_data(df_lag)
        self.assertEqual(len(X_train), int(95 * 0.7))
        self.assertEqual(len(X_test), 95 - int(95 * 0.7))
        self.assertEqual(X_train.shape[1], 5)  # 5 lag features

    def test_scale_features(self):
        df_lag = self.preprocessor.create_lag_features(self.df)
        X_train, y_train, X_test, y_test = self.preprocessor.split_data(df_lag)
        X_train_scaled, X_test_scaled = self.preprocessor.scale_features(X_train, X_test)
        self.assertEqual(X_train_scaled.shape, X_train.shape)
        self.assertEqual(X_test_scaled.shape, X_test.shape)
        # Verificar que la media de X_train_scaled es aproximadamente 0
        self.assertAlmostEqual(X_train_scaled.mean(), 0, places=1)

class TestModelTrainer(unittest.TestCase):
    def setUp(self):
        X, y = make_regression(n_samples=100, n_features=5, noise=0.1)
        self.X_train = X
        self.y_train = y
        self.trainer = ModelTrainer()

    def test_train_and_predict(self):
        self.trainer.train(self.X_train, self.y_train)
        predictions = self.trainer.predict(self.X_train)
        self.assertEqual(len(predictions), len(self.y_train))
        # Verificar que las predicciones sean números
        self.assertTrue(all(isinstance(p, float) for p in predictions))

    def test_evaluate(self):
        self.trainer.train(self.X_train, self.y_train)
        predictions = self.trainer.predict(self.X_train)
        mse = self.trainer.evaluate(self.y_train, predictions)
        self.assertIsInstance(mse, float)
        self.assertGreaterEqual(mse, 0)

class TestPipeline(unittest.TestCase):
    def setUp(self):
        X, y = make_regression(n_samples=100, n_features=1, noise=0.1)
        self.df = pd.DataFrame({'Price': y})
        self.pipeline = Pipeline(lags=5, train_size=0.7)

    def test_run_pipeline(self):
        result = self.pipeline.run(self.df)
        self.assertIn('model', result)
        self.assertIn('mse', result)
        self.assertIn('predictions', result)
        self.assertIn('X_test_scaled', result)
        self.assertIn('y_test', result)
        self.assertIsInstance(result['model'], xgb.XGBRegressor)
        self.assertIsInstance(result['mse'], float)
        self.assertIsInstance(result['predictions'], pd.DataFrame)

if __name__ == '__main__':
    unittest.main()