from myUnet import *
import scipy.misc
import skimage.measure
import cv2

myunet = myUnet()
model = myunet.Model
model.load_weights('unet5.hdf5')

num = 213    #这里填写样本数量
Path = os.path.dirname(os.path.realpath(__file__))
Imgs_Test = np.ndarray((1, 256, 256, 1), dtype=np.float32)
Predict = np.ndarray((num,256,256), dtype=np.float32)
Rate_All = np.ndarray((num), dtype=np.float32)
Rate_Part = np.ndarray((num), dtype=np.float32)

for m in range(256):
    for n in range(256):
        Imgs_Test[0][m][n][0] = 0
        for i in range(num):
            Predict[i][m][n] = 0
            Rate_All[i] = Rate_Part[i] = 0

for i in range(num):
    All_fenzi = 0
    All_fenmu = 256 * 216
    Part_fenzi = 0
    Part_fenmu = 0

    CorrectResult = cv2.imread(Path + "\\All\\" + str(i+1) + "result.jpg", cv2.IMREAD_GRAYSCALE)
    CorrectResult = np.uint8(CorrectResult[:, :])
    CorrectResult = img_to_array(CorrectResult)

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

    pic = Predict[i] * 255 / 2.0
    scipy.misc.imsave(Path + '\\results\\' + str(i+1) + '.jpg', pic)

    Ans = skimage.measure.label(Predict[i],connectivity = 2)
    Num = np.max(Ans)
    Vector = np.ndarray(Num)
    for x in range(Num):
        Vector[x] = 0
    for m in range(256):
        for n in range(256):
            if (Ans[m][n] > 0):
                Vector[Ans[m][n] - 1] = Vector[Ans[m][n] - 1] + 1

    select = np.where(Vector == np.max(Vector))
    select = select[0][0] + 1
    for m in range(256):
        for n in range(256):
            if (Ans[m][n] == select):
                Ans[m][n] = 255;
            else:
                Ans[m][n] = 0;

    for m in range(256):
        for n in range(216):
            if (CorrectResult[m][n] > 200):
                Part_fenmu = Part_fenmu + 1
                if (Ans[m][n+20] == 255):
                    All_fenzi = All_fenzi + 1
                    Part_fenzi = Part_fenzi + 1
            if (CorrectResult[m][n] < 50 and Ans[m][n+20] == 0):
                All_fenzi = All_fenzi + 1

    scipy.misc.imsave(Path + '\\results2\\' + str(i+1) + '.jpg', Ans)
    Rate_All[i]=All_fenzi/All_fenmu*1.0
    Rate_Part[i] = Part_fenzi / Part_fenmu * 1.0
    print("All_rate"+str(i)+":",Rate_All[i])
    print("Part_rate"+str(i)+":",Rate_Part[i])

print("Average All rate:",np.mean(Rate_All))
print("Average Part rate:",np.mean(Rate_Part))









