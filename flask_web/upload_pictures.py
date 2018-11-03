# https://blog.csdn.net/dcrmg/article/details/81987808?utm_source=blogxgwz0
# get post用阿嘎https://blog.csdn.net/qq_39974381/article/details/80927642
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify,send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
from datetime import timedelta
from flask_bootstrap import Bootstrap

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg'])


def allowed_file(filename):
    return ',' in filename and filename.rsplit(',', 1)[1] in ALLOWED_EXTENSIONS
app = Flask(__name__)
bootstrap=Bootstrap(app)
# 设置静态文件缓存的过期时间
app.send_file_max_age_default = timedelta(seconds=1)

basepath = os.path.dirname(__file__)
@app.route('/upload', methods=['POST', 'GET'])   # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
        path = basepath + "/static/photos/"
        file_path = path + f.filename  # 图片路径和名称
        print(file_path)
        f.save(file_path)  # 保存图片

        # 到本地文件读取图片并且显示在网页上
        img = cv2.imread(file_path)
        # 根据图片名字进行存储，但显示有问题
        # cv2.imwrite(os.path.join(file_path), img)   # 保存图片，第一个参数是路径加图像名，第二个是图像矩阵
        # 将图片名字都更改为test.jpg
        cv2.imwrite(os.path.join(path, 'test.jpg'), img)
        return render_template('upload_ok.html')
    return render_template('upload.html')



# 选择分割方式，radio实现
@app.route('/choose', methods=['get','post'])  # form表单中的action对应的是 网址！！不是函数名
def choosemmmm():
    segment = request.values.get('segment_way')
    if segment == 'auto':
         return redirect(url_for('auto_segment'))  # url_for后面加的是函数名
    if segment =='manual':
        return redirect(url_for('manual_segment'))

    # return render_template('upload_ok.html')      ## 可有可无？？？

@app.route('/auto_segment')
def auto_segment():
    return render_template('auto_segment.html')


@app.route('/manual_segment')
def manual_segment():
    return render_template('manual_segment.html')


# 自动分割里的图片下载, 网址需要加上文件名

# 如何根据显示的照片进行下载？？？？？？？？？？？？？？？？？？？将显示的照片赋值给filename???
@app.route('/download/<filename>', methods=['get'])
def download(filename):
    if request.method=="GET":
        if os.path.isfile(os.path.join('upload', filename)):
            return send_from_directory('upload', filename, as_attachment=True)


if __name__ =='__main__':
    app.run(debug=True)

