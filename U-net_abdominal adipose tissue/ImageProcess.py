import cv2
import pydicom
import numpy as np
import os
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

class myImageProcess(object):
    def __init__(self, StartNumber=0, EndNumber=403,DicomPath="\All"):
        self.Path = os.path.dirname(os.path.realpath(__file__)) + DicomPath
        #print("The File Path is:",self.Path)
        self.StartNumber = StartNumber
        self.EndNumber = EndNumber
        self.PicNum = self.EndNumber - self.StartNumber + 1
        self.ImgDatas = np.ndarray((self.PicNum, 512, 512, 1), dtype=np.float32)
        self.Label = np.ndarray((self.PicNum, 512, 512, 1), dtype=np.uint8)
        self.ImgLabels = np.ndarray((self.PicNum, 512, 512, 3), dtype=np.uint8)

    def LoadFile(self):
        print("************ Load File ************")
        for i in range(self.PicNum):
            dcm = pydicom.read_file(self.Path+"\IM"+str(self.StartNumber+i))
            pix = dcm.pixel_array
            pix = np.float32(pix)
            max = np.max(pix)
            pix = np.divide(pix,max)
            pix = img_to_array(pix)
            self.ImgDatas[i] = pix

            label = cv2.imread(self.Path+"\IM"+str(self.StartNumber+i)+".png",cv2.IMREAD_GRAYSCALE)
            label = np.uint8(label[:, :])
            label = img_to_array(label)
            self.Label[i] = label

    def LoadImageFile(self):
        print("************ Load File ************")
        for i in range(self.PicNum):
            dcm = pydicom.read_file(self.Path + "\IM" + str(self.StartNumber + i))
            pix = dcm.pixel_array
            pix = np.float32(pix)
            max = np.max(pix)
            pix = np.divide(pix, max)
            pix = img_to_array(pix)
            self.ImgDatas[i] = pix

    def DealLabel(self):
        print("************ Deal Label ************")
        for i in range(self.PicNum):    #n张图片
            for m in range(512):
                for n in range(512):
                    if( (255-self.Label[i][m][n][0])<15):
                        self.ImgLabels[i][m][n] = [1,0,0]          #背景255, 241-255
                    elif( (self.Label[i][m][n][0]-0)<20):
                        self.ImgLabels[i][m][n] = [1,0,0]           #NAT非脂肪组织0, 0-19
                    elif( self.Label[i][m][n][0]>134 ):
                        self.ImgLabels[i][m][n]= [0,0,1]        #SAT皮下脂肪组织225&165, 135-240
                    else:
                        self.ImgLabels[i][m][n] = [0,1,0]         #VAT内脏脂肪组织103&67, 20-134
            print(i,":finish!")

    def SaveData(self):
        np.save(os.path.dirname(os.path.realpath(__file__)) + '/Imgs_Train.npy', self.ImgDatas)
        np.save(os.path.dirname(os.path.realpath(__file__)) + '/Labels_Train.npy', self.ImgLabels)


if __name__ == "__main__":	#__name__ 是当前模块名，当模块被直接运行时模块名为 __main__ 。这句话的意思就是，
							#当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。
    MyImage = myImageProcess()
    #MyImage.LoadFile()
    MyImage.LoadImageFile()
    MyImage.DealLabel()
    MyImage.SaveData()
    print("For debug: Stop here!")