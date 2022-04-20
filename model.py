from unittest import result
from keras_facenet import FaceNet
import pathlib #このモジュールを使用するとファイルのパスをオブジェクトとして処理することができる
import numpy as np
from mira import core, detectors
from annoy import AnnoyIndex


#　浮世絵のベクトルデータ

# ①埋め込みベクトルの取得
embedder = FaceNet()

# ②画像のロード
dir_path = "./static/images/" #後ろに写真を取ってくるのでimagesの後にスラッシュ入れる

image_path_list = []
for img_path in pathlib.Path(dir_path).glob("*.jpg"):
    image_path_list.append(img_path)
image_path_list.sort()


# ③顔領域の特徴抽出（顔画像の切り取りと埋め込みベクトルの処理）
detector = detectors.MTCNN()
features = [] #顔の特徴ベクトル集合のfeatures
for image_path in image_path_list: #リストの中からパスを一つずつ取り出す
    image = core.Image.read(str(image_path)) #取り出した画像パスを読み込む
    embeddings = embedder.embeddings([image]) #一枚の画像をベクトルに変換する
    features.append(embeddings[0]) #featuresの箱にembeddingsの集合ベクトルを代入

features = np.array(features)  # 顔の特徴ベクトル集合のfeaturesは(N, 512)のサイズの二次元配列になる

# Annoyの実装
dim = 512
n_trees = 10

# ④ベクトル化した集合にインデックスを付ける
#indexは全部のベクトルが入っている大きな箱
index = AnnoyIndex(dim, 'euclidean') # dim:インデックスの次元, metric:距離の種類（ユーグリット距離・コサイン類似度のときは'euclidean'）
for i, feature in enumerate(features): #数字と中身をセットで変更してくれるenumerate関数
  index.add_item(i, feature) # インデックスに順番にベクトルを追加（検索対象となるベクトルの登録）
index.build(n_trees, n_jobs=-1) # インデックスをビルド（登録されたベクトルに対する検索を高速化するための構造の作成）
index.save('feature.ann') #上でビルドしたindexに名付ける


#以下の処理を関数化-（新しくロードされた写真と浮世絵を解析し、似てる浮世絵を返す処理）
def predict(image_path):  #（）内は変数なのでimage_pathには自分の顔写真が入る
  index.load('feature.ann')
  image = core.Image.read(str(image_path)) #画像を画像パスに変換して読み込み
  faces = detector.detect(image) #画像を顔領域の切り取り

  if not faces: # 画像は必ずしも顔領域が検出されるとは限らないため、検出されなかった場合は処理のスキップを行う
    print("not detect face", image_path)

  else:
    face = max(
      faces,
      key=lambda face: face.selection.area()
      ) # 複数の顔領域が検出されてしまうこともあるため、ここでは最大面積の領域の顔を代表の顔として利用する
    cropped_face = face.selection.extract(image) # 検出された顔領域の切り取り
    embeddings = embedder.embeddings([cropped_face]) # 埋め込みベクトルの取得
    feature = embeddings[0]
    feature = np.array(feature)  # 顔の特徴ベクトル集合のfeaturesは(N, 512)のサイズ
    
    v = feature
    n = 1
    print(index.get_nns_by_vector(v, n))

    #画像のパスを表示
    results = index.get_nns_by_vector(v, n)
    results2 = []
    ukiyoe = []

    for results2 in results:
      images = image_path_list[results2]
      print(images)
      ukiyoe.append(images)

  return ukiyoe


  
#関数の基礎
# def tashizan(A,B):
#   C = A + B
#   return C

# tashizan(1.2)



