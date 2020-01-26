import numpy as np

from skimage import feature
from PIL import Image
from skimage.color import rgb2gray


def get_edges(image_path):
    img_arr = np.array(Image.open(image_path), dtype=np.uint8)
    gray_image = rgb2gray(img_arr)
    return feature.canny(gray_image)
