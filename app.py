from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import os

# for color clustering
import PIL
from PIL import Image
import sklearn
from sklearn.cluster import KMeans

# for ajax
from flask_cors import CORS

# for image
import base64
from io import BytesIO

# for s3
import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET

ROOT_PATH = os.getcwd()
# 画像の仮アップロード先のディレクトリ
UPLOAD_FOLDER = ROOT_PATH + '/tmp'

app = Flask(
    __name__,
    static_folder = "./dist/static", 
    template_folder="./dist"
)
app.config.from_object(__name__)
CORS(app)
s3 = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', defaults={'path': ''})

@app.route('/<path:path>')
def catch(path):
    return render_template("index.html")

# クラスタごとの割合を計算
def centroid_histgram(clt):
  # clt.labels_ ... 各ピクセルが何番目のクラスタに属するか
  numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
  # ヒストグラムを計算
  (hist, _) = np.histogram(clt.labels_, bins = numLabels)
  hist = hist.astype('float')
  hist /= hist.sum() / 100
  return hist

# クラスタリング実行
def color_clustering(filename, k):
    if filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cv2_img = cv2.imread(file_path)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        # (縦、横、カラーチャンネル)->(縦と横をフラット化した値、カラーチャンネル)に変換
        cv2_img = cv2_img.reshape((cv2_img.shape[0] * cv2_img.shape[1], 3))
        # k-means方でクラスタリング
        cluster = KMeans(n_clusters=k)
        cluster.fit(X=cv2_img)
        result = cluster.cluster_centers_.astype(int)
        return {'color_list': result.tolist(), 'histogram': centroid_histgram(cluster).tolist()}

@app.route('/display_img', methods=['POST'])
def display_img():
    return jsonify(os.listdir(app.config['UPLOAD_FOLDER']))

@app.route('/uploads', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.form['file']
        dec_file = base64.b64decode(file.split(',')[1])
        dec_img = Image.open(BytesIO(dec_file))
        # 画像を圧縮
        resize_width = 640
        img_width, img_height = dec_img.size
        resize_height = resize_width / img_width * img_height
        dec_img = dec_img.resize((int(resize_width), int(resize_height)))
        # ファイルを保存
        filename = secure_filename(request.form['filename'])
        dec_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # s3に保存
        s3.put_object(
            Body=dec_file,
            Bucket=S3_BUCKET,
            Key='upload/' + filename,
            ContentType=request.form['filetype']
        )
        # クラスタリング実行
        return jsonify(color_clustering(filename, int(request.form['cluster'])))

# We only need this for local development.
if __name__ == '__main__':
    app.run()
