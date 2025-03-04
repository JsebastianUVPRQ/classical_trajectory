import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter

# Parámetros
b = 1.0
Omega = 1.0
t_max = 2 * np.pi  # Tiempo total
num_frames = 200
t = np.linspace(0, t_max, num_frames)

# Trayectoria
x = b * np.exp(Omega * t) * np.cos(Omega * t)
y = b * np.exp(Omega * t) * np.sin(Omega * t)
z = np.zeros_like(t)

# Configurar figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
max_xyz = b * np.exp(Omega * t_max) * 1.1
ax.set_xlim(-max_xyz, max_xyz)
ax.set_ylim(-max_xyz, max_xyz)
ax.set_zlim(-1, 1)

# Elementos del gráfico
line, = ax.plot([], [], [], lw=1, color='blue')
point, = ax.plot([], [], [], 'ro', markersize=5)

# Inicialización
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    point.set_data([], [])
    point.set_3d_properties([])
    return line, point,

# Actualización por frame
def update(frame):
    x_current = x[:frame+1]
    y_current = y[:frame+1]
    z_current = z[:frame+1]
    line.set_data(x_current, y_current)
    line.set_3d_properties(z_current)
    point.set_data([x_current[-1]], [y_current[-1]])
    point.set_3d_properties([z_current[-1]])
    return line, point,


# Crear animación
ani = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, interval=50)

# Guardar GIF
ani.save('3d_trajectory.gif', writer=PillowWriter(fps=20))
plt.close()