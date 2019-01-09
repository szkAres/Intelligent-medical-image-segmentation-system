import cv2
from keras.preprocessing.image import img_to_array
import keras.backend
from myUnet3 import *
from tensorflow import Graph, Session
import scipy.misc

class MyPredictBrain():
    def __init__(self):
        self.basepath = os.path.dirname(__file__)
        self.Imgs_Test = np.ndarray((1, 512, 512, 1), dtype=np.float32)
        self.Predict = np.ndarray((512, 512), dtype=np.float32)

        keras.backend.clear_session()  # 用于重复使用模型
        self.graph = Graph()
        with self.graph.as_default():
            self.session = Session()
            with self.session.as_default():
                unet = myUnet3()
                self.model = unet.Model
                self.model.load_weights('Unet_Brain.hdf5')

    def LoadPic(self):
        self.img = cv2.imread(self.basepath + "/static/auto_photos/auto_picture.jpg", cv2.IMREAD_GRAYSCALE)
        self.img = cv2.resize(self.img, (512,512), interpolation=cv2.INTER_NEAREST)
        pix = np.float32(self.img)
        max = np.max(pix)
        pix = np.divide(pix, max)
        pix = img_to_array(pix)
        for i in range(512):
            for j in range(512):
                self.Imgs_Test[0][i][j] = pix[i][j]

    def PredictPic(self):
        K.set_session(self.session)
        with self.graph.as_default():
            self.Result = self.model.predict(self.Imgs_Test, verbose=1)

    def SavePic(self):
        for m in range(512):
            for n in range(512):
                if ((self.Result[0][m][n][0] >= self.Result[0][m][n][1])and(self.Result[0][m][n][0] >= self.Result[0][m][n][2])):
                    self.Predict[m][n] = 0
                elif(self.Result[0][m][n][1] >= self.Result[0][m][n][2]):
                    self.Predict[m][n] = 127.5
                else:
                    self.Predict[m][n] = 255
        # scipy.misc.imsave(self.basepath + '\\1.jpg', self.Predict)

        path = self.basepath + "/static/after_auto_brain_photo/"
        cv2.imwrite(os.path.join(path, 'after_auto_brain_temp.jpg'), self.Predict)


if __name__ == "__main__":
    Predict = MyPredictBrain()
    Predict.LoadPic()
    Predict.PredictPic()
    Predict.SavePic()
