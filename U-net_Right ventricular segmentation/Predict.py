from myUnet import *
import scipy.misc

myunet = myUnet()
model = myunet.SetUnet()
model.load_weights('unet.hdf5')

num = 213    #这里填写样本数量
Path = os.path.dirname(os.path.realpath(__file__))
Imgs_Test = np.ndarray((1, 256, 256, 1), dtype=np.float32)
Predict = np.ndarray((num,256,256), dtype=np.float32)

for i in range(num):
    dcm = pydicom.read_file(Path + "\\All\\"+str(i+1)+".dcm")
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
                Predict[i][m][n] = 0
            else:
                Predict[i][m][n] = 1

    print(i,"\n")
    pic = Predict[i] * 255 / 2.0
    scipy.misc.imsave(Path + '\\results\\' + str(i) + '.jpg', pic)

np.save(Path+'\\Predict.npy',Predict)







