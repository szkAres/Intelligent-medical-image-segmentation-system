from myUnet import *
import scipy.misc

myunet = myUnet()
model = myunet.SetUnet()
model.load_weights('unet6.hdf5')

num = 404    #这里填写样本数量
Path = os.path.dirname(os.path.realpath(__file__))
Imgs_Test = np.ndarray((1, 512, 512, 1), dtype=np.float32)
Predict = np.ndarray((num,512,512), dtype=np.float32)

for i in range(num):
    dcm = pydicom.read_file(Path + "\\All\\IM"+str(i))
    pix = dcm.pixel_array
    pix = np.float32(pix)
    max = np.max(pix)
    pix = np.divide(pix, max)
    pix = img_to_array(pix)
    Imgs_Test[0] = pix
    Imgs_Test = Imgs_Test.astype('float32')

    imgs_mask_test = model.predict(Imgs_Test,verbose=1)

    for m in range(512):
        for n in range(512):
            if((imgs_mask_test[0][m][n][0]>=imgs_mask_test[0][m][n][1]) & (imgs_mask_test[0][m][n][0]>=imgs_mask_test[0][m][n][2])):
                Predict[i][m][n] = 0
            elif(imgs_mask_test[0][m][n][1]>=imgs_mask_test[0][m][n][2]):
                Predict[i][m][n] = 1
            else:
                Predict[i][m][n] = 2

    print(i,"\n")
    pic = Predict[i] * 255 / 2.0
    scipy.misc.imsave(Path + '\\results_predict\\' + str(i) + '.jpg', pic)

np.save(Path+'\\Predict.npy',Predict)







