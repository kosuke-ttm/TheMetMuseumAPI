# モジュールを読み込む
import json
import random
import urllib.parse
import urllib.request
from IPython.display import Image, display

# 受け取ったURLにHTTPリクエストを行い、そのURLが存在する場合に辞書型データを返す関数（存在しない場合は空の辞書型データを返す）
def request_data(url):
#エラーが発生すると思われるコード
  try:
    #URL取得
    response = urllib.request.urlopen(url)
  #エラー発生時の処理
  except urllib.error.HTTPError:
    return {}
  # エラーが発生しなかったときの処理
  else:
    #URLの中身を読み込む
    data = response.read()
    #辞書型に変換
    return json.loads(data)

print('※　キーワードは反映されない可能性があります．')
while True:
  # 検索条件の指定
  location = input('\nどの国の作品を見ますか英語で入力してください(例：Japan)>>')
  keyword = input('キーワードを入力してください（例：dog,cat)>>')

  # URLエンコード
  location = urllib.parse.quote(location)
  keyword = urllib.parse.quote(keyword)

  # 検索条件に関するデータを取得
  url_search = 'https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&geoLocation=' + location + '&q=' + keyword 
  data_search = request_data(url_search)


  # 検索条件に該当する作品がある場合、辞書からランダムでIDを指定し、作品の詳細データを取得する
  total = data_search['total']
  data_object = {}
  if total > 0:
    index = random.randint(0, total - 1)
    id = data_search['objectIDs'][index]

    url_object = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/' + str(id)
    data_object = request_data(url_object)
  else:
    print('対象作品がないのでもう一度違う国名またはキーワードを入力してください')
    continue 
  # Webページがある場合，URLエンコード
  image = ''
  if data_object:
    title = data_object['title']
    image = data_object['primaryImageSmall']
    image = urllib.parse.quote(image, safe=':/')
  else:
    print('Webページないのでもう一度違う国名またはキーワードを入力してください') 
    continue
  # Webページに画像データがある場合、ダウンロードする
  if image:
    #画像ファイルをimage.jpgとしてダウンロード
    urllib.request.urlretrieve(image, 'image.jpg')
    # 画像ファイル読み込み
    img = Image('image.jpg')

    #作品情報を表示
    print('\n作品ID :', id)
    print('タイトル :', title)
    # 画像の表示
    display(img)
    break
  else:
    print('画像がないのでもう一度違う国名またはキーワードを入力してください')
    continue