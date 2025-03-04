import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Definir constantes
b = 1.0  # Constante b
Omega = 1.0  # Constante Omega
t_max = 2 * np.pi / Omega  # Tiempo máximo para graficar una vuelta completa
num_points = 500  # Número de puntos para la gráfica

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

# Convertir componentes radiales y tangenciales a cartesianas
v_x = v_r * np.cos(theta) - v_theta * np.sin(theta)
v_y = v_r * np.sin(theta) + v_theta * np.cos(theta)
a_x = a_r * np.cos(theta) - a_theta * np.sin(theta)
a_y = a_r * np.sin(theta) + a_theta * np.cos(theta)

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-np.max(r), np.max(r))
ax.set_ylim(-np.max(r), np.max(r))
ax.set_aspect('equal')
ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
ax.axvline(0, color='black', linewidth=0.5, linestyle='--')
ax.set_title("Trayectoria de la partícula con vectores velocidad y aceleración")
ax.set_xlabel("x")
ax.set_ylabel("y")

# Elementos de la animación
particle, = ax.plot([], [], 'ro', label="Partícula")  # Partícula
trajectory, = ax.plot([], [], 'b-', label="Trayectoria")  # Trayectoria
velocity_vector = ax.quiver([], [], [], [], color='green', angles='xy', scale_units='xy', scale=1, label="Velocidad")
acceleration_vector = ax.quiver([], [], [], [], color='red', angles='xy', scale_units='xy', scale=1, label="Aceleración")
angle_text = ax.text(0.05, 0.95, "", transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

# Función de inicialización
def init():
    particle.set_data([], [])
    trajectory.set_data([], [])
    velocity_vector.set_UVC([], [])
    acceleration_vector.set_UVC([], [])
    angle_text.set_text("")
    return particle, trajectory, velocity_vector, acceleration_vector, angle_text

# Función de actualización
def update(frame):
    # Actualizar posición de la partícula
    particle.set_data(x[frame], y[frame])
    
    # Actualizar trayectoria
    trajectory.set_data(x[:frame+1], y[:frame+1])
    
    # Actualizar vector velocidad
    velocity_vector.set_UVC(v_x[frame], v_y[frame])
    velocity_vector.set_offsets((x[frame], y[frame]))
    
    # Actualizar vector aceleración
    acceleration_vector.set_UVC(a_x[frame], a_y[frame])
    acceleration_vector.set_offsets((x[frame], y[frame]))
    
    # Calcular el ángulo entre velocidad y aceleración
    dot_product = v_x[frame] * a_x[frame] + v_y[frame] * a_y[frame]
    v_magnitude = np.sqrt(v_x[frame]**2 + v_y[frame]**2)
    a_magnitude = np.sqrt(a_x[frame]**2 + a_y[frame]**2)
    cos_angle = dot_product / (v_magnitude * a_magnitude)
    angle = np.arccos(cos_angle)
    
    # Mostrar el ángulo en la animación
    angle_text.set_text(f"Ángulo: {np.degrees(angle):.1f}°")
    
    return particle, trajectory, velocity_vector, acceleration_vector, angle_text

# Crear la animación
ani = FuncAnimation(fig, update, frames=num_points, init_func=init, blit=True)

# Guardar la animación como un GIF
writer = PillowWriter(fps=30)
ani.save("particle_trajectory.gif", writer=writer)

plt.legend()
plt.show()
