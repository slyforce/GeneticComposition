import matplotlib
import Image
import numpy as np
import matplotlib.image

def save_image(array, filename):
  if not filename.endswith(".png"):
    filename += ".png"

  img = Image.fromarray(array, mode='L')
  img.save(filename)

  matplotlib.image.imsave(filename, array)