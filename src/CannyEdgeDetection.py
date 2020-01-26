# https://scikit-image.org/docs/dev/auto_examples/edges/plot_canny.html

# https://stackoverflow.com/questions/48491712/read-image-file-in-python-and-compute-canny-edge-filters

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage import feature

from PIL import Image
from skimage.color import rgb2gray

#load color image
img_rgb = '../resouces/maxresdefault.jpg'
img_arr = np.array(Image.open(img_rgb), dtype=np.uint8)


im = rgb2gray(img_arr)

# Compute the Canny filter for two values of sigma
edges1 = feature.canny(im)
edges2 = feature.canny(im, sigma=3)

for x in np.nditer(edges1):
    if x == True:
        print(x)

# display results
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                    sharex=True, sharey=True)

ax1.imshow(im, cmap=plt.cm.gray)
ax1.axis('off')
ax1.set_title('noisy image', fontsize=20)

ax2.imshow(edges1, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('Canny filter, $\sigma=1$', fontsize=20)

ax3.imshow(edges2, cmap=plt.cm.gray)
ax3.axis('off')
ax3.set_title('Canny filter, $\sigma=3$', fontsize=20)

fig.tight_layout()

plt.show()


#does not seem to work with pictures containing excessive black or white