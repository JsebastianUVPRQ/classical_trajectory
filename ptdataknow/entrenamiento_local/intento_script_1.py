import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Cargar los datos desde el CSV
df = pd.read_csv('ruta_del_archivo.csv')

# Convertir la columna de fecha a tipo datetime
df['fecha'] = pd.to_datetime(df['fecha'])

# Establecer la columna 'fecha' como índice
df.set_index('fecha', inplace=True)

# Mostrar una breve descripción de los datos
print(df.head())

# Si hay valores nulos, los eliminamos o rellenamos
df = df.dropna()

# Graficar la serie temporal
plt.figure(figsize=(10, 6))
plt.plot(df['precio'], label='Precio')
plt.title('Serie Temporal de Precio')
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.legend()
plt.show()

# División de los datos en conjunto de entrenamiento y prueba
train, test = train_test_split(df['precio'], test_size=0.2, shuffle=False)

# Crear y entrenar el modelo ARIMA (p, d, q) con parámetros (1,1,1) como ejemplo
model = ARIMA(train, order=(1, 1, 1))
model_fit = model.fit()

# Realizar predicciones sobre el conjunto de prueba
predictions = model_fit.forecast(steps=len(test))

# Calcular el error de la predicción
mse = mean_squared_error(test, predictions)
print(f"Error cuadrático medio (MSE): {mse}")

# Graficar las predicciones y los valores reales
plt.figure(figsize=(10, 6))
plt.plot(test.index, test, label='Precio Real', color='blue')
plt.plot(test.index, predictions, label='Predicción', color='red')
plt.title('Predicción de Serie Temporal')
plt.xlabel('Fecha')
plt.ylabel('Precio')
plt.legend()
plt.show()

# Predecir valores futuros (por ejemplo, los próximos 10 días)
future_predictions = model_fit.forecast(steps=10)
print("Predicciones futuras: ", future_predictions)
