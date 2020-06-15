# CARLAの操作方法

# Reference

- [First Step](https://carla.readthedocs.io/en/latest/core_world/)

## 1st. World and client

ClientとWorldはCARLAの2つの基本要素で、シミュレーションとそのアクターを操作するために必要な抽象化になる。
CARLAのサイトでは、要素の基本と作成の定義から、それらの可能性について説明されている。


## The Client

クライアントは、CARLAアーキテクチャの主要な要素の1つ。サーバーに接続し、情報を取得し、コマンドの変更を行う。変更は、スクリプトを介して行う。クライアントはクライアント自身の機能に応じて、Worldに接続してシミュレーションを操作する。

## Client creation

Clientがサーバーへ接続するには、以下の方法を用いる。

```python
client = carla.Client('localhost', 2000)
```

必要なのは接続先のIPアドレス、およびサーバーと通信するためのTCPポート。オプションとして、3番目のパラメーターは、作業スレッドの量を設定する。デフォルトでは、これはすべて（0）に設定されています。
上記のコードは、ループバックアドレスと接続ポート2000を示していtる。

```python
client.set_timeout(10.0) # seconds
```

Clientが作成できたら、接続タイムアウトを設定します。これによってすべてのネットワーク操作が制限されるため、これらの操作によってクライアントが永久にブロックされることはない。接続に失敗するとエラーが返される。

一度に複数のスクリプトを実行するのが一般的らしく、多くのClientを接続することが可能とのことだが、
最大接続数については要検証。

## Sample code to connect to the server

```python

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

def main():
    try:
        # ループバックアドレス指定で、接続ポートを2000で設定
        client = carla.Client('localhost', 2000)
        # 接続のタイムアウト時間を2秒指定
        client.set_timeout(2.0)

        #
        # <何らかの処理を記述する>
        #

    finally:
        print('終了処理')
        print('done.')

if __name__ == '__main__':
    main()

```

1. sys.path.append()は、CARLAのPythonAPIをローカルパッケージを指定して、ライブラリを読み込めるように指定。CARLAのビルド済みインストールすると、PythonAPIフォルダ下に配置されているので、配置されている場所までのパスを指定する。

2. main()関数内のcarla.Client()とclient.set_timeout()でサーバーへの接続を開始。


## World connection

Clientがサーバーへ接続できると、クライアントは現在のWorld情報を簡単に取得できる。

```py
world = client.get_world()
print(client.get_available_maps())
world = client.load_world('Town01')
```

## Sample code to get world infomation

```python
import carla

def main():
    try:
        # ループバックアドレス指定で、接続ポートを2000で設定
        client = carla.Client('localhost', 2000)
        # 接続のタイムアウト時間を2秒指定
        client.set_timeout(2.0)

        # Worldオブジェクトを取得
        world = client.get_world()
        # サーバーで利用可能なマップ情報して、ログ表示
        print(client.get_available_maps())

        # アクティブなワールドオブジェクトではなく、Town01を指定して、Worldオブジェクトを取得
        world = client.load_world('Town01')

        #
        # <何らかの処理を記述する>
        #

    finally:
        print('終了処理')
        print('done.')

if __name__ == '__main__':
    main()

```

1. クライアントで接続できている場合には、client.get_world()でシミュレーションで現在アクティブなワールドオブジェクトを取得する。
2. client.load_world()では、client.get_world()と違い、MAP情報を指定してWorldオブジェクトを取得する。


## Weather

WeatherParametersクラスは、World内の天気を操作することができる。
WeatherParametersクラスは、carla.Worldに適用できる照明と気象の仕様を含むオブジェクトを定義している。Worldオブジェクトに指定したい天気の状態を指定できる。

```python
weather = carla.WeatherParameters(
    cloudiness=80.0,
    precipitation=30.0,
    sun_altitude_angle=70.0)

world.set_weather(weather)

print(world.get_weather())
```

### Sample code to set weather

```python
import carla

def main():
    try:
        # ループバックアドレス指定で、接続ポートを2000で設定
        client = carla.Client('localhost', 2000)
        # 接続のタイムアウト時間を2秒指定
        client.set_timeout(2.0)

        # Worldオブジェクトを取得
        world = client.get_world()
        # サーバーで利用可能なマップ情報して、ログ表示
        print(client.get_available_maps())

        # アクティブなワールドオブジェクトではなく、Town01を指定して、Worldオブジェクトを取得
        world = client.load_world('Town01')

        # 天気情報の指定
        weather = carla.WeatherParameters(
        cloudiness=80.0,
        precipitation=30.0,
        sun_altitude_angle=70.0)

        # Worldオブジェクトに天気の情報を指定
        world.set_weather(weather)

        # Worldオブジェクトの現在の天気情報を取得
        print(world.get_weather())

    finally:
        print('終了処理')
        print('done.')

if __name__ == '__main__':
    main()
```
