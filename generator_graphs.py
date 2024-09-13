import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation as ani

# evaluar si existe la carpeta graphs_gif. Si no existe, crearla
# Ruta del directorio a crear
directorio_a_crear = 'graphs_gif'

# Obtener la ruta del script actual
ruta_script = os.path.dirname(os.path.abspath(__file__))

# Combinar la ruta del script con el nombre del directorio a crear
ruta_completa = os.path.join(ruta_script, directorio_a_crear)

# Verificar si el directorio ya existe
if not os.path.exists(ruta_completa):
    try:
        # Crear el directorio si no existe
        os.makedirs(ruta_completa)
        print(f'Directorio "{directorio_a_crear}" creado exitosamente en {ruta_script}')
    except OSError as e:
        print(f'Error al crear el directorio "{directorio_a_crear}": {e}')
else:
    print(f'El directorio "{directorio_a_crear}" ya existe en {ruta_script}')

# Definir la curva r(t)
def r(t):
    x = t*np.cos(t)
    y = t*np.sin(t)
    z = t
    return x, y, z

# Calcular la derivada de r(t) respecto a t
def dr_dt(t):
    dx_dt = np.cos(t) - t*np.sin(t)
    dy_dt = np.sin(t) + t*np.cos(t)
    dz_dt = 1
    return dx_dt, dy_dt, dz_dt
# Calculamos la segunda derivada de r(t) respecto a t
def d2r_dt2(t):
    dx2_dt2 = -2*np.sin(t) - t*np.cos(t)
    dy2_dt2 = 2*np.cos(t) - t*np.sin(t)
    dz2_dt2 = 0
    return dx2_dt2, dy2_dt2, dz2_dt2

# Normalizar un vector
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

# Punto en la curva
t_punto = 0

punto = r(t_punto)

# Vectores tangente, normal y binormal en el punto
# tangente = r'(t) / |r'(t)|
tangente = normalize(dr_dt(t_punto))

# vector normal   r' x (r'' x r') / |r'||r'' x r'| TENTATIVA
'''
v1 = normalize(np.cross(d2r_dt2(t_punto), dr_dt(t_punto)))
v2 = normalize(dr_dt(t_punto))
normal = np.cross(v2, v1)
'''
v1 = dr_dt(t_punto)
v2 = np.cross(d2r_dt2(t_punto), dr_dt(t_punto))
normal = normalize(np.cross(v1, v2))

# Binormal     PROBAR EN FUNCION DE r, r' y r''
binormal = normalize(np.cross(dr_dt(t_punto), d2r_dt2(t_punto)))

# Graficar la curva
t_vals = np.linspace(0, 2 * np.pi, 100)

# Graficar el punto en la curva
scale_factor = 1

    
'''
ax.scatter(punto[0], punto[1], punto[2], color='red', label='x,y,z')
# Graficar los vectores tangente, normal y binormal
scale_factor = 1
ax.quiver(punto[0], punto[1], punto[2], tangente[0], tangente[1], tangente[2], color='blue', label='T', length=scale_factor)
ax.quiver(punto[0], punto[1], punto[2], normal[0], normal[1], normal[2], color='green', label='N', length=scale_factor)
ax.quiver(punto[0], punto[1], punto[2], binormal[0], binormal[1], binormal[2], color='purple', label='B', length=scale_factor)

La característica que diferencia a este fragmento de código del anterior es que en este caso se grafica un solo punto en la curva, mientras que en el fragmento anterior se graficaban todos los puntos de la curva. Además, en este caso se grafican los vectores tangente, normal y binormal en el punto especificado.
'''
# --------------bucle for para graficar el punto y los vectores tangente, normal y binormal------------
for i in range(0, len(t_vals)):
    # Crear la figura
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    curve = np.array([r(t) for t in t_vals]).T
    ax.plot(curve[0], curve[1], curve[2], label='r(t)')
    
    punto = r(t_vals[i])
    tangente = normalize(dr_dt(t_vals[i]))
    v1 = dr_dt(t_vals[i])
    v2 = np.cross(d2r_dt2(t_vals[i]), dr_dt(t_vals[i]))
    normal = normalize(np.cross(v1, v2))
    binormal = normalize(np.cross(dr_dt(t_vals[i]), d2r_dt2(t_vals[i])))
    ax.scatter(punto[0], punto[1], punto[2], color='red', label='x,y,z')
    ax.quiver(punto[0], punto[1], punto[2], tangente[0], tangente[1], tangente[2], color='blue', label='T', length=scale_factor)
    ax.quiver(punto[0], punto[1], punto[2], normal[0], normal[1], normal[2], color='green', label='N', length=scale_factor)
    ax.quiver(punto[0], punto[1], punto[2], binormal[0], binormal[1], binormal[2], color='purple', label='B', length=scale_factor)
    # Configurar el aspecto de la gráfica
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    #guardar la imagen usando plt.savefig y os
    plt.savefig(os.path.join('graphs_gif', f'frame_{i}.png'))
    #limpiar la figura en cada iteracion
    ax.clear()
    plt.close(fig)