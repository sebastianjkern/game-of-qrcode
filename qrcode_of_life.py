# %%
import functools
import qrcode

import numpy

import matplotlib.pyplot as plt

from PIL import Image
from PIL import ImageOps

@functools.cache
def get_mat(data):        
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.border = 0

    return qr.get_matrix()

data = """
Das Spielfeld ist in Zeilen und Spalten unterteilt und im Idealfall unendlich groß.
Jedes Gitterquadrat ist ein zellulärer Automat (Zelle), der einen von zwei Zuständen 
einnehmen kann, welche oft als lebendig und tot bezeichnet werden. Zunächst wird eine 
Anfangsgeneration von lebenden Zellen auf dem Spielfeld platziert."""

# %%

generations = 100

mat = numpy.array(get_mat(data), numpy.bool)

im = ImageOps.invert(Image.fromarray(mat).resize((mat.shape[0] * 10, mat.shape[1] * 10), resample=Image.ANTIALIAS).convert("L"))
im.save("image_" + str(0).zfill(3) +".png")

new = numpy.array([[False] * len(mat[0])] * len(mat), numpy.bool)

for gen in range(1, generations+1):
    for xi, _ in enumerate(mat):
        for yi, _ in enumerate(mat[0]):
            sum = 0

            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        continue

                    if xi+x >= len(mat) or yi+y >= len(mat[0]):
                        continue

                    if (mat[xi + x][yi + y]):
                        sum += 1
                        
            if sum < 2:
                new[xi][yi] = False

            if sum >= 4:
                new[xi][yi] = False

            if sum == 2:
                new[xi][yi] = mat[xi][yi]

            if sum == 3:
                new[xi][yi] = True

    mat = new

    im = ImageOps.invert(Image.fromarray(new).resize((new.shape[0] * 10, new.shape[1] * 10), resample=Image.ANTIALIAS).convert("L"))
    im.save("image_" + str(gen).zfill(3) +".png")

    new = numpy.array([[False] * len(mat[0])] * len(mat), numpy.bool)
