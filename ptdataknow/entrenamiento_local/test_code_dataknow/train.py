import xgboost as xgb
from sklearn.metrics import mean_squared_error
import pandas as pd

class ModelTrainer:
    def __init__(self, params=None):
        if params is None:
            params = {
                'objective': 'reg:squarederror',
                'n_estimators': 3000,
                'max_depth': 4,
                'learning_rate': 0.001,
                'colsample_bytree': 0.3,
                'reg_alpha': 0.1,
                'reg_lambda': 0.1
            }
        self.params = params
        self.model = xgb.XGBRegressor(**self.params)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, y_true, y_pred):
        mse = mean_squared_error(y_true, y_pred)
        return mse

    def get_model(self):
        return self.model