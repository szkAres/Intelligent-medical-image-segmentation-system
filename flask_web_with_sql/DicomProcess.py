import pydicom
import os
import numpy as np
import cv2

DefaultCenter = 0 #For IM0.dcm, DefaultCenter = 352.5
DefaultWidth = 0  #For IM0.dcm, DefaultWidth = 705.0
#pathTest = 'E:/Document/Intelligent-medical-image-segmentation-system/flask_web_with_sql/static/manual_photos/IM104.dcm'

class MyDicomPreProcess():
    def __init__(self):
        self.basepath = os.path.dirname(__file__)

    def ImportPic(self,pathSet):
        self.OriginalPic = pydicom.read_file(pathSet)
        self.Pixel = self.OriginalPic.pixel_array
        self.Pixel = np.float32(self.Pixel)

        global DefaultCenter,DefaultWidth
        DefaultCenter = 0.5 * ( np.max(self.Pixel) + np.min(self.Pixel) )
        DefaultWidth = np.max(self.Pixel) - np.min(self.Pixel)

    def ChangeWindowCenterAndWidth(self, Center=-1, Width=-1):
        global DefaultWidth,DefaultCenter
        if(Center<0):
            Center = DefaultCenter
        if(Width<0):
            Width = DefaultWidth

        size = self.Pixel.shape
        self.ChangedPic = np.ndarray((512, 512), dtype=np.float32)
        min = (2 * Center - Width) / 2.0
        max = (2 * Center + Width) / 2.0
        for i in range(size[0]):
            for j in range(size[1]):
                if(self.Pixel[i][j] < min):
                    self.ChangedPic[i][j] = 0
                elif(self.Pixel[i][j] > max):
                    self.ChangedPic[i][j] = 255
                else:
                    self.ChangedPic[i][j] =(self.Pixel[i][j] - min)*255/(max-min)

    def SavePic(self):
        cv2.imwrite(self.basepath+'//static/manual_photos/manual_picture_window_changed.jpg', self.ChangedPic)

# if __name__ =='__main__':
#     myPreProcess = MyDicomPreProcess()
#     myPreProcess.ImportPic(pathTest)
#     #myPreProcess.ChangeWindowCenterAndWidth()    #使用覆盖所有像素范围的default窗宽窗位
#     myPreProcess.ChangeWindowCenterAndWidth(Center=500,Width=500) #指定窗宽窗位
#     #myPreProcess.ChangeWindowCenterAndWidth(Center=352.5,Width=705) #指定窗宽窗位
#     #myPreProcess.ChangeWindowCenterAndWidth(Center=200,Width=900) #指定窗宽窗位
#     myPreProcess.SavePic()

