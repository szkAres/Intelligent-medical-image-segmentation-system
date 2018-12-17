import cv2
import pydicom
import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

class myImageProcess(object):
    def __init__(self, StartNumber=1, EndNumber=213,DicomPath="\All"):
        self.Path = os.path.dirname(os.path.realpath(__file__)) + DicomPath
        #print("The File Path is:",self.Path)
        self.StartNumber = StartNumber
        self.EndNumber = EndNumber
        self.PicNum = self.EndNumber - self.StartNumber + 1
        self.ImgDatas = np.ndarray((self.PicNum, 256, 256, 1), dtype=np.float32)
        self.Label = np.ndarray((self.PicNum, 256, 256, 1), dtype=np.uint8)
        self.ImgLabels = np.ndarray((self.PicNum, 256, 256, 2), dtype=np.uint8)

    def LoadFile(self):
        print("************ Load File ************")
        for i in range(self.PicNum):
            dcm = pydicom.read_file(self.Path+"//"+str(self.StartNumber+i)+".dcm")
            pix = dcm.pixel_array
            pix = np.float32(pix)
            max = np.max(pix)
            pix = np.divide(pix,max)
            pix = img_to_array(pix)
            print(i)
            for m in range(256):
                for n in range(216):
                    self.ImgDatas[i][m][n+20] = pix[m][n]

            mlabel = cv2.imread(self.Path+"\\"+str(self.StartNumber+i)+"result.jpg",cv2.IMREAD_GRAYSCALE)
            mlabel = np.uint8(mlabel[:, :])
            mlabel = img_to_array(mlabel)
            for m in range(256):
                for n in range(216):
                    self.Label[i][m][n+20]  = mlabel[m][n]

    def LoadImageFile(self):
        print("************ Load File ************")
        for i in range(self.PicNum):
            dcm = pydicom.read_file(self.Path + "\\" + str(self.StartNumber + i)+".dcm")
            pix = dcm.pixel_array
            pix = np.float32(pix)
            max = np.max(pix)
            pix = np.divide(pix, max)
            pix = img_to_array(pix)
            self.ImgDatas[i] = pix

    def DealLabel(self):
        print("************ Deal Label ************")
        for i in range(self.PicNum):    #n张图片
            for m in range(256):
                for n in range(256):
                    if( self.Label[i][m][n][0]<50):
                        self.ImgLabels[i][m][n] = [1,0]          #背景0
                    else:
                        self.ImgLabels[i][m][n] = [0,1]          #右心室255
            print(i,":finish!")

    def SaveData(self):
        np.save(os.path.dirname(os.path.realpath(__file__)) + '/Imgs_Train.npy', self.ImgDatas)
        np.save(os.path.dirname(os.path.realpath(__file__)) + '/Labels_Train.npy', self.ImgLabels)


if __name__ == "__main__":	#__name__ 是当前模块名，当模块被直接运行时模块名为 __main__ 。这句话的意思就是，
							#当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。
    MyImage = myImageProcess()
    MyImage.LoadFile()
    #MyImage.LoadImageFile()
    MyImage.DealLabel()
    MyImage.SaveData()
    print("For debug: Stop here!")