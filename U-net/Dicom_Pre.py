import pydicom
import numpy as np
import os
from skimage import data, exposure, img_as_float

Path = os.path.dirname(os.path.realpath(__file__))
pixel = np.ndarray((100, 512, 512), dtype=np.uint8)

for i in range(100):
    dcm = pydicom.read_file(Path + "\\ALL_fuben\\IM" + str(i))
    pix = dcm.pixel_array
    pix = np.uint16(pix)

    pix = exposure.adjust_gamma(pix, 1.1)  # 调暗(如果小于1，则为调亮)

    dcm.PixelData = pix.tostring()
    dcm.save_as(Path+'\\All\\IM'+str(i))
