# https://blog.csdn.net/dcrmg/article/details/81987808?utm_source=blogxgwz0
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
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


@app.route('/upload', methods=['POST', 'GET'])   # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
        # print('f is:', not(f))  # not f false, f为true
        # print('allowed_file(f.filename):',allowed_file(f.filename))

        # if not(f and allowed_file(f.filename)):
        # return jsonify({"error":1001, "msg":"请检查上传的图片类型！！！！！"})

        user_input = request.form.get("name")

        # 根据当前的文件位置进行存储，双斜线问题会报错
        basepath = os.path.dirname(__file__)
        # upload_path = os.path.join(basepath, '/static/images/', secure_filename(f.filename))

        # 要在本地创建文件夹，将存放照片的位置固定
        # 将上传的图片存到本地文件夹中
        upload_path = os.path.join('E:/pycharm_projects/flask_first_web/static/images/', secure_filename(f.filename))
        print('upload_path', upload_path)
        f.save(upload_path)
        # 使用opencv转换一下图片格式和名称，为了方便在upload_ok中进行图片的显示
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
        return render_template('upload_ok.html', userinput=user_input)
    return render_template('upload.html')


if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)