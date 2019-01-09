from myUnet3 import *
import scipy.misc
import skimage.measure

Path = os.path.dirname(os.path.realpath(__file__))
Imgs_Test = np.ndarray((1, 256, 256, 1), dtype=np.float32)
Predict = np.ndarray((256,256), dtype=np.float32)
for m in range(256):
    for n in range(256):
        Imgs_Test[0][m][n][0]=0
        Predict[m][n]=0

myunet = myUnet()
model = myunet.Model
model.load_weights('unet5.hdf5')

dcm = pydicom.read_file(Path + "\\All\\32.dcm")
pix = dcm.pixel_array
pix = np.float32(pix)
max = np.max(pix)
pix = np.divide(pix, max)
pix = img_to_array(pix)
for m in range(256):
    for n in range(216):
        Imgs_Test[0][m][n + 20] = pix[m][n]
Imgs_Test = Imgs_Test.astype('float32')
imgs_mask_test = model.predict(Imgs_Test,verbose=1)

for m in range(256):
    for n in range(256):
        if((imgs_mask_test[0][m][n][0]>=imgs_mask_test[0][m][n][1])):
            Predict[m][n] = 0
        else:
            Predict[m][n] = 1

pic = Predict* 255
scipy.misc.imsave(Path + '\\1.jpg', pic)

Ans = skimage.measure.label(Predict,connectivity = 2)
Num = np.max(Ans)
Vector = np.ndarray(Num)
for i in range(Num):
    Vector[i]=0
for m in range(256):
    for n in range(256):
        if(Ans[m][n]>0):
            Vector[Ans[m][n]-1] = Vector[Ans[m][n]-1]+1
select = np.where(Vector == np.max(Vector))
select = select[0][0]+1
for m in range(256):
    for n in range(256):
        if (Ans[m][n] == select):
            Ans[m][n] = 255;
        else:
            Ans[m][n]=0;

scipy.misc.imsave(Path + '\\2.jpg', Ans)


