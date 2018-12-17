# https://blog.csdn.net/dcrmg/article/details/81987808?utm_source=blogxgwz0
# get post用阿嘎https://blog.csdn.net/qq_39974381/article/details/80927642
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify,send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import datetime
from flask_bootstrap import Bootstrap
from medical_image import medical_image
from class_user import class_user
import Class_Predict
import pydicom
import numpy as np
from DicomProcess import *

host = "localhost"
username = "root"
password = "temppwd"
database_name = "flask_sql"
table_name = "ImagesDatabase"
user_table_name = "UsersDatabase"
user_temp = 'Ray'
type_temp = 'fat'

manual_picture_path_global = '/'

app = Flask(__name__)
bootstrap = Bootstrap(app)

mPredict = Class_Predict.MyPredict()

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg','dcm'])
def allowed_file(filename):
    return ',' in filename and filename.rsplit(',', 1)[1] in ALLOWED_EXTENSIONS

# 设置静态文件缓存的过期时间
app.send_file_max_age_default = datetime.timedelta(seconds=1)
basepath = os.path.dirname(__file__)

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_login = request.form['username']
        password_login = request.form['password']
        
        user_login = class_user(username_login)
        user_login.connect_to_database(host,username,password,database_name)
        user_login.user_check(user_table_name)
        user_login.disconnect_database()
        
        if user_login.exist == False:
            return jsonify({'status': '-1', 'errmsg': 'user does not exist!'})
        elif password_login == user_login.Password:
            global user_temp
            user_temp = user_login.User
            return redirect(url_for('choose'))  # url_for后面加的是函数名
        else :
            return jsonify({'status': '-1', 'errmsg': 'password is wrong!'})

    return render_template('login.html')

# 用户登录
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username_register = request.form['register_username']
        password_register = request.form['register_password']
        re_password_register = request.form['register_re_password']
        
        user_register = class_user(username_register)
        user_register.connect_to_database(host,username,password,database_name)
        user_register.user_check(user_table_name)
        user_register.disconnect_database()
        
        if user_register.exist == True:
            return jsonify({'status': '-1', 'errmsg': 'user exists!'})
        else:
            if password_register == re_password_register:
                registerTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                user_register.connect_to_database(host,username,password,database_name)
                user_register.user_create(user_table_name,password_register,registerTime,False)
                user_register.disconnect_database()
                return redirect(url_for('login'))
            else:
                return jsonify({'status': '-1', 'errmsg': 'password is not same!'})

    return render_template('register.html')

# 选择分割方式，radio实现
@app.route('/choose', methods=['get','post'])  # form表单中的action对应的是 网址！！不是函数名
def choose():
    segment = request.values.get('segment_way')
    if segment == 'auto':
         return redirect(url_for('auto_segment'))
    if segment =='manual':
        return redirect(url_for('manual_segment'))
    return render_template('choose_method.html')

# 选择分割方式，radio实现
@app.route('/windowChoose', methods=['get','post'])  # form表单中的action对应的是 网址！！不是函数名
def windowChoose():
    if request.method == 'POST':
        centerSet = request.form['center']
        widthSet = request.form['width']
        centerSetF = float(centerSet)
        widthSetF = float(widthSet)
        myPreProcess = MyDicomPreProcess()
        myPreProcess.ImportPic(manual_picture_path_global)
        myPreProcess.ChangeWindowCenterAndWidth(Center=centerSetF,Width=widthSetF)
        myPreProcess.SavePic()
    '''
    chooseType = request.values.get('windowChooseType')
    if chooseType == 'type1':
         myPreProcess = MyDicomPreProcess()
         myPreProcess.ImportPic(manual_picture_path_global)
         myPreProcess.ChangeWindowCenterAndWidth(Center=500,Width=500)
         myPreProcess.SavePic()
    if chooseType =='type2':
         myPreProcess = MyDicomPreProcess()
         myPreProcess.ImportPic(manual_picture_path_global)
         myPreProcess.ChangeWindowCenterAndWidth(Center=352,Width=705)
         myPreProcess.SavePic()
    if chooseType =='type3':
         myPreProcess = MyDicomPreProcess()
         myPreProcess.ImportPic(manual_picture_path_global)
         myPreProcess.ChangeWindowCenterAndWidth(Center=200,Width=900)
         myPreProcess.SavePic()
    '''
    
    return render_template('Big_Little_Drag_Function.html')

# 自动分割处理图片上传
@app.route('/auto_segment', methods=['POST', 'GET'])   # 添加路由
def auto_segment():
    if request.method == 'POST':
        f = request.files['file']
        path = basepath + "/static/auto_photos/"
        file_path = path + f.filename  # 图片路径和名称
        print(file_path)
        f.save(file_path)  # 保存图片
        # 到本地文件读取图片并且显示在网页上
        (shotname, extension) = os.path.splitext(f.filename);
        if (extension == '.dcm'):
            dcm = pydicom.read_file(file_path)
            img = dcm.pixel_array
            img = np.float32(img)
        else:
            img = cv2.imread(file_path)
        # 根据图片名字进行存储，但显示有问题
        # cv2.imwrite(os.path.join(file_path), img)   # 保存图片，第一个参数是路径加图像名，第二个是图像矩阵
        # 将图片名字都更改为test.jpg
        cv2.imwrite(os.path.join(path, 'auto_picture.jpg'), img)
        return render_template('auto_segment_upload.html')
    return render_template('auto_segment.html')

# 自动分割后的图片显示


# 选择分割类型(腹部 or  颅脑  or  左心室)
@app.route('/segmentation_type', methods=['get','post'])  # form表单中的action对应的是 网址！！不是函数名
def segmentation_type():
    segment = request.values.get('segment_type')
    if segment == 'AAT':
         return redirect(url_for('auto_belly_segment'))  # url_for后面加的是函数名

@app.route('/auto_belly_segment')
def auto_belly_segment():
    mPredict.LoadPic()
    mPredict.PredictPic()
    mPredict.SavePic()
    return render_template('auto_belly_segment.html')

# 手动分割处理
@app.route('/manual_segment', methods=['POST', 'GET'])   # 添加路由
def manual_segment():
    if request.method == 'POST':
        f = request.files['file']
        path = basepath + "/static/manual_photos/"
        file_path = path + f.filename  # 图片路径和名称
        print(file_path)
        global manual_picture_path_global
        manual_picture_path_global = file_path
        
        print('uploading')
        nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        image_write = medical_image(user_temp,nowTime,type_temp,file_path)
        image_write.connect_to_database(host,username,password,database_name)
        image_write.insert(table_name)
        image_write.commit_database()
        image_write.disconnect_database()
        print('uploaded')
        
        f.save(file_path)  # 保存图片

        # 到本地文件读取图片并且显示在网页上
        (shotname, extension) = os.path.splitext(f.filename)
        if (extension == '.dcm'):
            dcm = pydicom.read_file(file_path)
            img = dcm.pixel_array
            img = np.float32(img)
        else:
            img = cv2.imread(file_path)
        cv2.imwrite(os.path.join(path, 'manual_picture.jpg'), img)
        return redirect(url_for('windowChoose')) 
    return render_template('manual_segment.html')

# 手动分割之后的图片上传到服务器
#@app.route('/upload_to_server', methods=['POST', 'GET'])

if __name__ =='__main__':
    app.run(debug=False)#,host='0.0.0.0', port=8000)

