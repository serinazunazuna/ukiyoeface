import os
from flask import (
     Flask, 
     request, 
     render_template)
from model import predict
#上記で同じディレクトリにあるPythonファイルの関数をインポート
#追記１
# import tensorflow.compat.v1 as tf
import tensorflow as tf
#追記２
# graph = tf.compat.v1.get_default_graph()
# graph = tf.get_default_graph()

#画像のアップロード先のディレクトリ
UPLOAD_FOLDER='./static/mypicture'

#FlaskでAPIを書くときのおまじない
app = Flask(__name__, static_folder='./static')

#ルーティング
@app.route('/')
def index():
    return render_template('index.html')

#受け取った画像をディレクトリに保存する
@app.route('/upload', methods=['GET', 'POST']) #画像を送信したときの処理。送信のaction='/upload'またメソッドを入れることでデータのやり取りができる


def upload_user_files():
    if request.method == 'POST':
        upload_file = request.files['upload_file'] #送られた画像ファイルをrequest.filesで受け取りupload_fileという変数に代入し、idを指定
        img_path = os.path.join(UPLOAD_FOLDER,upload_file.filename) #画像の保存先のパスを生成
        upload_file.save(img_path)
        ukiyoe = predict(img_path) 
        # global graph
        # with graph.as_default():
        #     images,image_path = predict(img_path)
        return render_template('result.html', ukiyoe_path=str(ukiyoe[0]), img_path=img_path) #一つ目が似てる浮世絵画像で２つ目は自分の画像



# おまじない
if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=5000)