# import cv2
# import numpy as np
# from keras.preprocessing.image import img_to_array
# import keras.backend
# from myUnet2 import *
# from tensorflow import Graph, Session
# import skimage.measure
# import scipy.misc
#
# class MyPredictRightVentricular():
#     def __init__(self):
#         self.basepath = os.path.dirname(__file__)
#         self.Imgs_Test = np.ndarray((1, 256, 256, 1), dtype=np.float32)
#         for i in range(256):
#             for j in range(256):
#                 self.Imgs_Test[0][i][j] = 0
#         self.Predict = np.ndarray((256, 216), dtype=np.float32)
#
#         keras.backend.clear_session()  # 用于重复使用模型
#         self.graph = Graph()
#         with self.graph.as_default():
#             self.session = Session()
#             with self.session.as_default():
#                 unet = myUnet2()
#                 self.model = unet.Model
#                 self.model.load_weights('Unet_RightVentricular.hdf5')
#
#     def LoadPic(self):
#        # self.img = cv2.imread(self.basepath + "/static/auto_photos/auto_picture.jpg", cv2.IMREAD_GRAYSCALE)
#         self.img = cv2.imread(self.basepath + "/auto_picture.jpg", cv2.IMREAD_GRAYSCALE)
#         pix = np.float32(self.img)
#         max = np.max(pix)
#         pix = np.divide(pix, max)
#         pix = img_to_array(pix)
#         for i in range(256):
#             for j in range(216):
#                 self.Imgs_Test[0][i][j+20] = pix[i][j]
#
#     def PredictPic(self):
#         K.set_session(self.session)
#         with self.graph.as_default():
#             self.Result = self.model.predict(self.Imgs_Test, verbose=1)
#
#     def SavePic(self):
#         for m in range(256):
#             for n in range(216):
#                 if ((self.Result[0][m][n+20][0] >= self.Result[0][m][n+20][1])):
#                     self.Predict[m][n] = 0
#                 else:
#                     self.Predict[m][n] = 1
#         Ans = skimage.measure.label(self.Predict, connectivity=2)
#         Num = np.max(Ans)
#         Vector = np.ndarray(Num)
#         for i in range(Num):
#             Vector[i] = 0
#         for m in range(256):
#             for n in range(216):
#                 if (Ans[m][n] > 0):
#                     Vector[Ans[m][n] - 1] = Vector[Ans[m][n] - 1] + 1
#         select = np.where(Vector == np.max(Vector))
#         select = select[0][0] + 1
#         for m in range(256):
#             for n in range(216):
#                 if (Ans[m][n] == select):
#                     Ans[m][n] = 255;
#                 else:
#                     Ans[m][n] = 0;
#                     scipy.misc.imsave(self.basepath + '\\1.jpg', Ans)
#                     # path = self.basepath + "/static/after_auto_ventricle_photo/"
#                     # cv2.imwrite(os.path.join(path, 'after_auto_ventricle_temp.jpg'), Ans)
# if __name__ == "__main__":
#     Predict = MyPredictRightVentricular()
#     Predict.LoadPic()
#     Predict.PredictPic()
#     Predict.SavePic()

import cv2
from keras.preprocessing.image import img_to_array
import keras.backend
from myUnet2 import *
from tensorflow import Graph, Session
import skimage.measure
import scipy.misc

class MyPredictRightVentricular():
    def __init__(self):
        self.basepath = os.path.dirname(__file__)
        self.Imgs_Test = np.ndarray((1, 256, 256, 1), dtype=np.float32)
        for i in range(256):
            for j in range(256):
                self.Imgs_Test[0][i][j] = 0
        self.Predict = np.ndarray((256, 216), dtype=np.float32)

        keras.backend.clear_session()  # 用于重复使用模型
        self.graph = Graph()
        with self.graph.as_default():
            self.session = Session()
            with self.session.as_default():
                unet = myUnet2()
                self.model = unet.Model
                self.model.load_weights('Unet_RightVentricular.hdf5')

    def LoadPic(self):
        self.img = cv2.imread(self.basepath + "/static/auto_photos/auto_picture.jpg", cv2.IMREAD_GRAYSCALE)
        self.img = cv2.resize(self.img, (256,216), interpolation=cv2.INTER_NEAREST)
        pix = np.float32(self.img)
        max = np.max(pix)
        pix = np.divide(pix, max)
        pix = img_to_array(pix)
        for i in range(256):
            for j in range(216):
                self.Imgs_Test[0][i][j+20] = pix[i][j]

    def PredictPic(self):
        K.set_session(self.session)
        with self.graph.as_default():
            self.Result = self.model.predict(self.Imgs_Test, verbose=1)

    def SavePic(self):
        for m in range(256):
            for n in range(216):
                if ((self.Result[0][m][n+20][0] >= self.Result[0][m][n+20][1])):
                    self.Predict[m][n] = 0
                else:
                    self.Predict[m][n] = 1
        Ans = skimage.measure.label(self.Predict, connectivity=2)
        Num = np.max(Ans)
        Vector = np.ndarray(Num)
        for i in range(Num):
            Vector[i] = 0
        for m in range(256):
            for n in range(216):
                if (Ans[m][n] > 0):
                    Vector[Ans[m][n] - 1] = Vector[Ans[m][n] - 1] + 1
        select = np.where(Vector == np.max(Vector))
        select = select[0][0] + 1
        for m in range(256):
            for n in range(216):
                if (Ans[m][n] == select):
                    Ans[m][n] = 255;
                else:
                    Ans[m][n] = 0;
                    #scipy.misc.imsave(self.basepath + '\\1.jpg', Ans)
                    # path = self.basepath + "/static/after_auto_ventricle_photo/"
                    # scipy.misc.imsave(path + 'after_auto_ventricle_temp.jpg', Ans)
        path = self.basepath + "/static/after_auto_ventricle_photo/"
        cv2.imwrite(os.path.join(path, 'after_auto_ventricle_temp.jpg'), Ans)



# if __name__ == "__main__":
#     Predict = MyPredictRightVentricular()
#     Predict.LoadPic()
#     Predict.PredictPic()
#     Predict.SavePic()
