import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Ensure the directory for saving GIF frames exists
def ensure_directory_exists(directory_name):
    """Check if a directory exists; if not, create it."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, directory_name)
    if not os.path.exists(full_path):
        try:
            os.makedirs(full_path)
            print(f'Directory "{directory_name}" created successfully at {script_dir}')
        except OSError as e:
            print(f'Error creating directory "{directory_name}": {e}')
    else:
        print(f'Directory "{directory_name}" already exists at {script_dir}')
    return full_path

# Define the curve r(t)
def r(t):
    x = t * np.cos(t)
    y = t * np.sin(t)
    z = t
    return x, y, z

# Derivative of r(t) with respect to t
def dr_dt(t):
    dx_dt = np.cos(t) - t * np.sin(t)
    dy_dt = np.sin(t) + t * np.cos(t)
    dz_dt = 1
    return dx_dt, dy_dt, dz_dt

# Second derivative of r(t) with respect to t
def d2r_dt2(t):
    dx2_dt2 = -2 * np.sin(t) - t * np.cos(t)
    dy2_dt2 = 2 * np.cos(t) - t * np.sin(t)
    dz2_dt2 = 0
    return dx2_dt2, dy2_dt2, dz2_dt2

# Normalize a vector
def normalize(v):
    norm = np.linalg.norm(v)
    return v / norm if norm != 0 else v

# Plot the curve and vectors at a specific point
def plot_frame(t_vals, i, output_dir, scale_factor=1):
    """Plot the curve and tangent, normal, binormal vectors at the ith point."""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Compute the curve points
    curve = np.array([r(t) for t in t_vals]).T
    ax.plot(curve[0], curve[1], curve[2], label='r(t)', color='black', linewidth=1)

    # Compute the current point and vectors
    punto = r(t_vals[i])
    tangente = normalize(dr_dt(t_vals[i]))
    v1 = dr_dt(t_vals[i])
    v2 = np.cross(d2r_dt2(t_vals[i]), dr_dt(t_vals[i]))
    normal = normalize(np.cross(v1, v2))
    binormal = normalize(np.cross(dr_dt(t_vals[i]), d2r_dt2(t_vals[i])))

    # Plot the point and vectors
    ax.scatter(*punto, color='red', label='Point (x, y, z)')
    ax.quiver(*punto, *tangente, color='blue', label='Tangent (T)', length=scale_factor)
    ax.quiver(*punto, *normal, color='green', label='Normal (N)', length=scale_factor)
    ax.quiver(*punto, *binormal, color='purple', label='Binormal (B)', length=scale_factor)

    # Configure the plot
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    # Save the frame
    frame_filename = os.path.join(output_dir, f'frame_{i:03d}.png')  # Use zero-padded filenames
    plt.savefig(frame_filename)
    plt.close(fig)

# Main function to generate frames
def main():
    # Ensure the output directory exists
    output_dir = ensure_directory_exists('graphs_trajectory_gif')

    # Define the parameter range for the curve
    t_vals = np.linspace(0, 2 * np.pi, 100)

    # Generate frames for each point on the curve
    for i in range(len(t_vals)):
        plot_frame(t_vals, i, output_dir)

if __name__ == "__main__":
    main()