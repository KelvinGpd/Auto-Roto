# https://github.com/Play3rZer0/EdgeDetect
# https://medium.com/hd-pro/applying-edge-detection-to-feature-extraction-and-pixel-integrity-2d39d9460842
from PIL import Image, ImageFilter, ImageChops

image = Image.open("../resouces/simple_duck.jpg");

image_edges = image.filter(ImageFilter.FIND_EDGES)

image_edges.show()