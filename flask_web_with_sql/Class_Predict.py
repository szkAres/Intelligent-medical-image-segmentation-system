import cv2
from keras.preprocessing.image import img_to_array
import keras.backend
from myUnet import *
from tensorflow import Graph, Session


class MyPredict():
    def __init__(self):
        self.basepath = os.path.dirname(__file__)
        self.Imgs_Test = np.ndarray((1, 512, 512, 1), dtype=np.float32)
        self.Predict = np.ndarray((512, 512), dtype=np.float32)

        keras.backend.clear_session()  # 用于重复使用模型
        self.graph = Graph()
        with self.graph.as_default():
            self.session = Session()
            with self.session.as_default():
                unet = myUnet()
                self.model = unet.Model
                self.model.load_weights('unet6.hdf5')

    def LoadPic(self):
        self.img = cv2.imread(self.basepath + "/static/auto_photos/auto_picture.jpg", cv2.IMREAD_GRAYSCALE)
        self.img = cv2.resize(self.img, (512,512), interpolation=cv2.INTER_NEAREST)
       # self.img = cv2.imread(self.basepath + "/static/photos/test.jpg", cv2.IMREAD_GRAYSCALE)

    def PredictPic(self):
        pix = np.float32(self.img)
        max = np.max(pix)
        pix = np.divide(pix, max)
        pix = img_to_array(pix)
        self.Imgs_Test[0] = pix

        K.set_session(self.session)
        with self.graph.as_default():
            self.Result = self.model.predict(self.Imgs_Test, verbose=1)

    def SavePic(self):
        for m in range(512):
            for n in range(512):
                if ((self.Result[0][m][n][0] >= self.Result[0][m][n][1]) & (self.Result[0][m][n][0] >= self.Result[0][m][n][2])):
                    self.Predict[m][n] = 0
                elif (self.Result[0][m][n][1] >= self.Result[0][m][n][2]):
                    self.Predict[m][n] = 122
                else:
                    self.Predict[m][n] = 255

        path = self.basepath + "/static/after_auto_belly_photo/"
        cv2.imwrite(os.path.join(path, 'after_auto_belly_temp.jpg'), self.Predict)

