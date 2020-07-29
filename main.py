from flask import Flask, render_template, request, jsonify
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

app = Flask(
    __name__,
    static_folder = "./dist/static", 
    template_folder="./dist"
)
app.config.from_object(__name__)
CORS(app)

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
def color_clustering(dec_img, k):
    cv2_img = cv2.imdecode(dec_img, cv2.IMREAD_ANYCOLOR)
    # 画像を縮小
    height = cv2_img.shape[0]
    width = cv2_img.shape[1]
    cv2_img = cv2.resize(cv2_img, (640, int(640 / int(width) * int(height)))) 
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
    # (縦、横、カラーチャンネル)->(縦と横をフラット化した値、カラーチャンネル)に変換
    cv2_img = cv2_img.reshape((cv2_img.shape[0] * cv2_img.shape[1], 3))
    # k-means方でクラスタリング
    cluster = KMeans(n_clusters=k)
    cluster.fit(X=cv2_img)
    result = cluster.cluster_centers_.astype(int)
    return {'color_list': result.tolist(), 'histogram': centroid_histgram(cluster).tolist()}

@app.route('/uploads', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.form['file']
        dec_file = base64.b64decode(file.split(',')[1])
        img_np = np.frombuffer(dec_file, np.uint8)
        return jsonify(color_clustering(img_np, int(request.form['cluster'])))

# We only need this for local development.
if __name__ == '__main__':
    app.run()
