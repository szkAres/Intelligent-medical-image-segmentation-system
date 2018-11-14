import cv2
from keras.preprocessing.image import img_to_array
from myUnet import *

basepath = os.path.dirname(__file__)

img = cv2.imread( basepath + "/static/photos/test.jpg", cv2.IMREAD_GRAYSCALE)
pix = np.float32(img)
max = np.max(pix)
pix = np.divide(pix, max)
pix = img_to_array(pix)
Imgs_Test = np.ndarray((1, 512, 512, 1), dtype=np.float32)
Imgs_Test[0] = pix

unet = myUnet()
model = unet.SetUnet()
model.load_weights('unet6.hdf5')

result = model.predict(Imgs_Test,verbose=1)

predict = np.ndarray((512, 512), dtype=np.float32)

for m in range(512):
    for n in range(512):
        if((result[0][m][n][0] >= result[0][m][n][1]) & (result[0][m][n][0] >= result[0][m][n][2])):
            predict[m][n] = 0
        elif(result[0][m][n][1] >= result[0][m][n][2]):
            predict[m][n] = 122
        else:
            predict[m][n] = 255

cv2.imwrite(basepath+'/predict.jpg', predict)







