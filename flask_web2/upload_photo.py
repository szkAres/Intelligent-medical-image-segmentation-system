# https://blog.csdn.net/weixin_36380516/article/details/80347192
# https://blog.csdn.net/kangkanglou/article/details/79036388

#   使用make_response进行图片的上传
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify,send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
from datetime import timedelta

# 设置允许的文件格式


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg'])


def allowed_file(filename):
    return ',' in filename and filename.rsplit(',', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存的过期时间


app.send_file_max_age_default = timedelta(seconds=1)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basepath = os.path.abspath(os.path.dirname(__file__))

@app.route('/upload', methods=['POST', 'GET'])   # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
        #basepath = os.path.dirname(__file__)
        path = basepath + "/static/photo/"
        file_path = path + f.filename  # 图片路径和名称
        print(file_path)
        f.save(file_path)  # 保存图片

        image_data = open(os.path.join(file_path), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response


        # 到本地文件读取图片并且显示在网页上
       # img = cv2.imread(file_path)
        #cv2.imwrite(os.path.join(file_path), img)   # 保存图片，第一个参数是路径加图像名，第二个是图像矩阵
# <img src="{{url_for('static', filename='./images/test.jpg')}}" width="400" height="400" alt="你的图片被外星人劫持~~"/>

        #return render_template('upload_ok.html')
    return render_template('upload.html')



# 选择分割方式，radio实现
@app.route('/choose', methods=['get','post'])  # form表单中的action对应的是 网址！！不是函数名
def choosemmmm():
    segment = request.values.get('segment_way')
    if segment == 'auto':
         return redirect(url_for('auto_segment'))  # url_for后面加的是函数名
    if segment =='manual':
        return redirect(url_for('manual_segment'))


@app.route('/show/<string:filename>', methods=['get'])
def show_photo(filename):
    file_dir = os.path.join(basepath, app.config['UPLOAD_FOLDER'])
    if request.method == 'get':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass


@app.route('/auto_segment')
def auto_segment():
    return render_template('auto_segment.html')


@app.route('/manual_segment')
def manual_segment():
    return render_template('manual_segment.html')


if __name__ =='__main__':
    app.run(debug=True)

