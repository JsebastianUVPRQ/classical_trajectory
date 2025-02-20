import os
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# ------------------------------------------PREPROCESS------------------------------------------


class DataPreprocessor:
    def __init__(self, lags=5, train_size=0.7):
        self.lags = lags
        self.train_size = train_size
        self.scaler = StandardScaler()

    def create_lag_features(self, df):
        df = df.copy()
        for lag in range(1, self.lags + 1):
            df[f'lag_{lag}'] = df['Price'].shift(lag)
        df = df.dropna().reset_index(drop=True)
        return df

    def split_data(self, df):
        train_size = int(len(df) * self.train_size)
        train, test = df.iloc[:train_size], df.iloc[train_size:]
        X_train = train.drop(columns=['Price'])
        y_train = train['Price']
        X_test = test.drop(columns=['Price'])
        y_test = test['Price']
        return X_train, y_train, X_test, y_test

    def scale_features(self, X_train, X_test):
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    
# ------------------------------------------preprocess------------------------------------------
# ------------------------------------------TRAINER------------------------------------------
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
# ------------------------------------------TRAINER------------------------------------------
# ------------------------------------------PIPELINE------------------------------------------
class Pipeline:
    def __init__(self, lags=5, train_size=0.7, model_params=None):
        self.preprocessor = DataPreprocessor(lags=lags, train_size=train_size)
        self.trainer = ModelTrainer(params=model_params)

    def run(self, df):
        # Preprocesar datos
        df_preprocessed = self.preprocessor.create_lag_features(df)
        X_train, y_train, X_test, y_test = self.preprocessor.split_data(df_preprocessed)
        X_train_scaled, X_test_scaled = self.preprocessor.scale_features(X_train, X_test)
        
        # Entrenar modelo
        self.trainer.train(X_train_scaled, y_train)
        
        # Hacer predicciones
        predictions = self.trainer.predict(X_train_scaled)
        futuros = pd.DataFrame(predictions, index=train.index, columns=['Prediction'])
        
        # Evaluar modelo
        mse = self.trainer.evaluate(y_train, predictions)
        print(f"Error cuadrático medio (MSE): {mse}")
        
        return {
            'model': self.trainer.get_model(),
            'mse': mse,
            'predictions': futuros,
            'X_test_scaled': X_test_scaled,
            'y_test': y_test
        }     


# USAR DATAFRAME "Y_modificado.csv"
path = os.getcwd()
dff = pd.read_csv('.\Y_modificado.csv', engine='python')

X_train, y_train, X_test, y_test = DataPreprocessor.split_data(df=dff)

pipeline = Pipeline(lags=5, train_size=0.7)
result = pipeline.run(df)

