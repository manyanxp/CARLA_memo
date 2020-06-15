# サンプルソース

```python
import glob
import os
import sys

try:
    sys.path.append(glob.glob('./dist/carla-*%d.%d-%s.egg' % (
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

        # クライアントバージョンとサーバーバージョンを取得
        print(f"client version: {client.get_client_version()} ")
        print(f"server version: {client.get_server_version()} ")
        # Worldオブジェクトを取得
        world = client.get_world()
        # サーバーで利用可能なマップを取得
        print(client.get_available_maps())
        
        # ex)
        # ['/Game/Carla/Maps/Town04', '/Game/Carla/Maps/Town05', 
        #   '/Game/Carla/Maps/Town01', '/Game/Carla/Maps/Town02', 
        #       '/Game/Carla/Maps/Town03']

        # マップ　Town01を読み込み
        world = client.load_world("Town01")

        # 天気の指定
        weather = carla.WeatherParameters(
            cloudiness=80.0,
            precipitation=30.0,
            sun_altitude_angle=70.0
        )
        # 天気の設定
        world.set_weather(weather)
        # 天気の情報取得
        print(world.get_weather())

    finally:
        print('終了処理')
        print('done.')

if __name__ == '__main__':
    main()
```