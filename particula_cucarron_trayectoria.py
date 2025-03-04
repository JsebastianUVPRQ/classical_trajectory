import numpy as np
import matplotlib.pyplot as plt

# Definir constantes
b = 1.0  # Constante b (puede ajustarse)
Omega = 1.0  # Constante Omega (puede ajustarse)
t_max = 2 * np.pi / Omega  # Tiempo máximo para graficar una vuelta completa
num_points = 1000  # Número de puntos para la gráfica

# Definir el tiempo como un arreglo
t = np.linspace(0, t_max, num_points)

# Coordenadas polares r y theta
r = b * np.exp(Omega * t)
theta = Omega * t

# Convertir a coordenadas cartesianas
x = r * np.cos(theta)
y = r * np.sin(theta)

# Derivadas para calcular velocidad y aceleración
dr_dt = b * Omega * np.exp(Omega * t)  # dr/dt
dtheta_dt = Omega  # dtheta/dt
d2r_dt2 = b * Omega**2 * np.exp(Omega * t)  # d^2r/dt^2
d2theta_dt2 = 0  # d^2theta/dt^2

# Componentes radiales y tangenciales de la velocidad
v_r = dr_dt
v_theta = r * dtheta_dt

# Componentes radiales y tangenciales de la aceleración
a_r = d2r_dt2 - r * (dtheta_dt)**2
a_theta = r * d2theta_dt2 + 2 * dr_dt * dtheta_dt

# Magnitudes de velocidad y aceleración
v_magnitude = np.sqrt(v_r**2 + v_theta**2)
a_magnitude = np.sqrt(a_r**2 + a_theta**2)

# Producto punto entre velocidad y aceleración
dot_product = v_r * a_r + v_theta * a_theta

# Coseno del ángulo entre velocidad y aceleración
cos_angle = dot_product / (v_magnitude * a_magnitude)

# Ángulo entre velocidad y aceleración
angle = np.arccos(cos_angle)

# Verificar que el ángulo es siempre pi/4
assert np.allclose(angle, np.pi / 4), "El ángulo no es constante o no es pi/4"

# Graficar la trayectoria de la partícula
plt.figure(figsize=(8, 8))
plt.plot(x, y, label="Trayectoria de la partícula")
plt.scatter(x[0], y[0], color='red', label="Posición inicial")  # Posición inicial
plt.scatter(x[-1], y[-1], color='green', label="Posición final")  # Posición final
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
plt.xlabel("x")
plt.ylabel("y")
plt.title("Trayectoria de la partícula en coordenadas cartesianas")
plt.legend()
plt.grid()
plt.axis('equal')
plt.show()

# Mostrar el ángulo entre velocidad y aceleración
print(f"El ángulo entre los vectores velocidad y aceleración es siempre: {np.pi / 4} radianes (45 grados).")
