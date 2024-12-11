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