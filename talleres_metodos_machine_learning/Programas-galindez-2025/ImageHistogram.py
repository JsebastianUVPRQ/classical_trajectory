import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt

# Load the image
img = io.imread("../programas/images/IMG_3301.jpg", as_gray=True) * 255

# Display the image
fig, ax = plt.subplots(1, 1, figsize=(5,5))
ax.imshow(img, cmap="gray")
plt.show()

# Prepare the figure for the histograms
fig, axs = plt.subplots(1, 2, figsize=(12,4))

# Plot the first histogram
axs[0].hist(
    img.ravel(),           # The image must be flattened to use function hist
    bins=range(0,256,2)    # Define 128 bins between 0 and 255
)
axs[0].set_xlabel("Intensities")
axs[0].set_ylabel("Number")

# Plot the second histogram
axs[1].hist(
    img.ravel(),           # The image must be flattened to use function hist
    bins=range(0,256,16)   # Define 16 bins between 0 and 255
)
axs[1].set_xlabel("Intensities")
axs[1].set_ylabel("Number")

# Show the figure
plt.show()