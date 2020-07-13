# CARLAの操作方法

## Reference

- [First Step](https://carla.readthedocs.io/en/latest/core_world/)

## 1st. World and client

ClientとWorldはCARLAの2つの基本要素で、シミュレーションとそのアクターを操作するために必要な抽象化になる。
CARLAのサイトでは、要素の基本と作成の定義から、それらの可能性について説明されている。


### The Client

クライアントは、CARLAアーキテクチャの主要な要素の1つ。サーバーに接続し、情報を取得し、コマンドの変更を行う。変更は、スクリプトを介して行う。クライアントはクライアント自身の機能に応じて、Worldに接続してシミュレーションを操作する。

### Client creation

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

### ActorとBlueprints


> An actor is anything that plays a role in the simulation.

Actorは、シミュレーションで役割を果たすすべてのものになる。


> - Vehicles.
> - Walkers.
> - Sensors.
> - The spectator.
> - Traffic signs and traffic lights.

- 車両
- 歩行者
- センサ
- 観客
- 交通標識と信号機

> Blueprints are already-made actor layouts necessary to spawn an actor. Basically, models with animations and a set of attributes. Some of these attributes can be customized by the user, others don't. There is a Blueprint library containing all the blueprints available as well as information on them.

Blueprintは、ActorをSpawn(生み出す)するために必要な既製のActor Layoutです。基本的に、アニメーションと一連の属性を持つモデル。これらの属性には、ユーザーがカスタマイズできるものとそうでないものがあります。利用可能なすべてのBluprintsとそれらに関する情報を含むBlueprintライブラリがあります。

### Maps と navigation

> The map is the object representing the simulated world, the town mostly. There are eight maps available. All of them use OpenDRIVE 1.4 standard to describe the roads.

マップは、シミュレートされた世界、主に町を表すオブジェクトです。利用可能な8つのマップがあります。それらのすべては、道路を記述するためにOpenDRIVE 1.4標準を使用します。

> Roads, lanes and junctions are managed by the Python API to be accessed from the client. These are used along with the waypoint class to provide vehicles with a navigation path.

道路、車線、ジャンクションはPython APIによって管理され、クライアントからアクセスできます。これらはWaypoint Classと共に使用され、車両にナビゲーションパスを提供します。

> Traffic signs and traffic lights are accessible as carla.Landmark objects that contain information about their OpenDRIVE definition. Additionally, the simulator automatically generates stops, yields and traffic light objects when running using the information on the OpenDRIVE file. These have bounding boxes placed on the road. Vehicles become aware of them once inside their bounding box.

交通標識や信号機には、OpenDRIVE定義に関する情報を含むcarla.Landmarkオブジェクトとしてアクセスできます。さらに、シミュレーターは、OpenDRIVEファイルの情報を使用して実行すると、ストップ、降伏、信号機オブジェクトを自動的に生成します。これらには、道路に配置された境界ボックスがあります。車両は、バウンディングボックス内に入るとそれらを認識します。

### Sensors と data

> Sensors wait for some event to happen, and then gather data from the simulation. They call for a function defining how to manage the data. Depending on which, sensors retrieve different types of sensor data.

センサーは、イベントが発生するのを待ってから、シミュレーションからデータを収集します。データを管理する方法を定義する関数が必要です。センサーは、さまざまなタイプのセンサーデータを取得します。

> A sensor is an actor attached to a parent vehicle. It follows the vehicle around, gathering information of the surroundings. The sensors available are defined by their blueprints in the Blueprint library.

センサーは、親車両に取り付けられたActorです。周囲の車両を追跡し、周辺の情報を収集します。利用可能なセンサーは、ブループリントライブラリのブループリントによって定義されます。

> - Cameras (RGB, depth and semantic segmentation).
> - Collision detector.
> - Gnss sensor.
> - IMU sensor.
> - Lidar raycast.
> - Lane invasion detector.
> - Obstacle detector.
> - Radar.
> - RSS.


- カメラ（RGB、深度、と　セマティックセグメンテーション
- 衝突検知器
- Gnss センサー
- IMU センサー
- ライダー 指向性
- レーン侵入検知器
- 障害物検知器
- レイダー
- RSS

### Sample code to connect to the server

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


### World connection

Clientがサーバーへ接続できると、クライアントは現在のWorld情報を簡単に取得できる。

```py
world = client.get_world()
print(client.get_available_maps())
world = client.load_world('Town01')
```

### Sample code to get world infomation

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


### Weather

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

### Sample code to set double camera

This sample is based client_bounding_boxes.py from carla.

```python

#!/usr/bin/env python
# coding=utf-8

# Copyright (c) 2019 Aptiv
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
An example of client-side bounding boxes with basic car controls.

Controls:

    W            : throttle
    S            : brake
    AD           : steer
    Space        : hand-brake

    ESC          : quit
"""

# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================


import glob
import os
import sys
import logging

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================

import carla

import weakref
import random

try:
    import pygame
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_SPACE
    from pygame.locals import K_a
    from pygame.locals import K_d
    from pygame.locals import K_s
    from pygame.locals import K_w
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

logging.basicConfig(level = logging.INFO,
                   format='[%(asctime)s][%(levelname)s][%(module)s.%(funcName)s] -> %(message)s')

VIEW_WIDTH = 1920//4
VIEW_HEIGHT = 1080//4
VIEW_WIDTH2 = 1920//4
VIEW_HEIGHT2 = 1080//4
DISPLAY_WIDTH = VIEW_WIDTH + VIEW_WIDTH2
DISPLAY_HEIGHT = VIEW_HEIGHT
VIEW_FOV = 90

BB_COLOR = (248, 64, 24)

logging.info("CAMERA1 (W,H)({},{})".format(VIEW_WIDTH,VIEW_HEIGHT ))
logging.info("CAMERA2 (W,H)({},{})".format(VIEW_WIDTH2,VIEW_HEIGHT2 ))

# ==============================================================================
# -- ClientSideBoundingBoxes ---------------------------------------------------
# ==============================================================================


class ClientSideBoundingBoxes(object):
    """
    This is a module responsible for creating 3D bounding boxes and drawing them
    client-side on pygame surface.
    """

    @staticmethod
    def get_bounding_boxes(vehicles, camera):
        """
        Creates 3D bounding boxes based on carla vehicle list and camera.
        """

        bounding_boxes = [ClientSideBoundingBoxes.get_bounding_box(vehicle, camera) for vehicle in vehicles]
        # filter objects behind camera
        bounding_boxes = [bb for bb in bounding_boxes if all(bb[:, 2] > 0)]
        return bounding_boxes

    @staticmethod
    def draw_bounding_boxes(display, bounding_boxes):
        """
        Draws bounding boxes on pygame display.
        """

        bb_surface = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))
        bb_surface.set_colorkey((0, 0, 0))
        for bbox in bounding_boxes:
            points = [(int(bbox[i, 0]), int(bbox[i, 1])) for i in range(8)]
            # draw lines
            # base
            pygame.draw.line(bb_surface, BB_COLOR, points[0], points[1])
            pygame.draw.line(bb_surface, BB_COLOR, points[0], points[1])
            pygame.draw.line(bb_surface, BB_COLOR, points[1], points[2])
            pygame.draw.line(bb_surface, BB_COLOR, points[2], points[3])
            pygame.draw.line(bb_surface, BB_COLOR, points[3], points[0])
            # top
            pygame.draw.line(bb_surface, BB_COLOR, points[4], points[5])
            pygame.draw.line(bb_surface, BB_COLOR, points[5], points[6])
            pygame.draw.line(bb_surface, BB_COLOR, points[6], points[7])
            pygame.draw.line(bb_surface, BB_COLOR, points[7], points[4])
            # base-top
            pygame.draw.line(bb_surface, BB_COLOR, points[0], points[4])
            pygame.draw.line(bb_surface, BB_COLOR, points[1], points[5])
            pygame.draw.line(bb_surface, BB_COLOR, points[2], points[6])
            pygame.draw.line(bb_surface, BB_COLOR, points[3], points[7])
        display.blit(bb_surface, (0, 0))

    @staticmethod
    def get_bounding_box(vehicle, camera):
        """
        Returns 3D bounding box for a vehicle based on camera view.
        """

        bb_cords = ClientSideBoundingBoxes._create_bb_points(vehicle)
        cords_x_y_z = ClientSideBoundingBoxes._vehicle_to_sensor(bb_cords, vehicle, camera)[:3, :]
        cords_y_minus_z_x = np.concatenate([cords_x_y_z[1, :], -cords_x_y_z[2, :], cords_x_y_z[0, :]])
        bbox = np.transpose(np.dot(camera.calibration, cords_y_minus_z_x))
        camera_bbox = np.concatenate([bbox[:, 0] / bbox[:, 2], bbox[:, 1] / bbox[:, 2], bbox[:, 2]], axis=1)
        return camera_bbox

    @staticmethod
    def _create_bb_points(vehicle):
        """
        Returns 3D bounding box for a vehicle.
        """

        cords = np.zeros((8, 4))
        extent = vehicle.bounding_box.extent
        cords[0, :] = np.array([extent.x, extent.y, -extent.z, 1])
        cords[1, :] = np.array([-extent.x, extent.y, -extent.z, 1])
        cords[2, :] = np.array([-extent.x, -extent.y, -extent.z, 1])
        cords[3, :] = np.array([extent.x, -extent.y, -extent.z, 1])
        cords[4, :] = np.array([extent.x, extent.y, extent.z, 1])
        cords[5, :] = np.array([-extent.x, extent.y, extent.z, 1])
        cords[6, :] = np.array([-extent.x, -extent.y, extent.z, 1])
        cords[7, :] = np.array([extent.x, -extent.y, extent.z, 1])
        return cords

    @staticmethod
    def _vehicle_to_sensor(cords, vehicle, sensor):
        """
        Transforms coordinates of a vehicle bounding box to sensor.
        """

        world_cord = ClientSideBoundingBoxes._vehicle_to_world(cords, vehicle)
        sensor_cord = ClientSideBoundingBoxes._world_to_sensor(world_cord, sensor)
        return sensor_cord

    @staticmethod
    def _vehicle_to_world(cords, vehicle):
        """
        Transforms coordinates of a vehicle bounding box to world.
        """

        bb_transform = carla.Transform(vehicle.bounding_box.location)
        bb_vehicle_matrix = ClientSideBoundingBoxes.get_matrix(bb_transform)
        vehicle_world_matrix = ClientSideBoundingBoxes.get_matrix(vehicle.get_transform())
        bb_world_matrix = np.dot(vehicle_world_matrix, bb_vehicle_matrix)
        world_cords = np.dot(bb_world_matrix, np.transpose(cords))
        return world_cords

    @staticmethod
    def _world_to_sensor(cords, sensor):
        """
        Transforms world coordinates to sensor.
        """

        sensor_world_matrix = ClientSideBoundingBoxes.get_matrix(sensor.get_transform())
        world_sensor_matrix = np.linalg.inv(sensor_world_matrix)
        sensor_cords = np.dot(world_sensor_matrix, cords)
        return sensor_cords

    @staticmethod
    def get_matrix(transform):
        """
        Creates matrix from carla transform.
        """

        rotation = transform.rotation
        location = transform.location
        c_y = np.cos(np.radians(rotation.yaw))
        s_y = np.sin(np.radians(rotation.yaw))
        c_r = np.cos(np.radians(rotation.roll))
        s_r = np.sin(np.radians(rotation.roll))
        c_p = np.cos(np.radians(rotation.pitch))
        s_p = np.sin(np.radians(rotation.pitch))
        matrix = np.matrix(np.identity(4))
        matrix[0, 3] = location.x
        matrix[1, 3] = location.y
        matrix[2, 3] = location.z
        matrix[0, 0] = c_p * c_y
        matrix[0, 1] = c_y * s_p * s_r - s_y * c_r
        matrix[0, 2] = -c_y * s_p * c_r - s_y * s_r
        matrix[1, 0] = s_y * c_p
        matrix[1, 1] = s_y * s_p * s_r + c_y * c_r
        matrix[1, 2] = -s_y * s_p * c_r + c_y * s_r
        matrix[2, 0] = s_p
        matrix[2, 1] = -c_p * s_r
        matrix[2, 2] = c_p * c_r
        return matrix


# ==============================================================================
# -- BasicSynchronousClient ----------------------------------------------------
# ==============================================================================


class BasicSynchronousClient(object):
    """
    Basic implementation of a synchronous client.
    """

    def __init__(self):
        self.client = None
        self.world = None
        self.camera = None
        self.camera2 = None
        self.car = None

        self.display = None
        self.display2 = None
        self.image = None
        self.capture = True

        self.image2 = None
        self.capture2 = True

    def camera_blueprint(self, width, height):
        """
        Returns camera blueprint.
        """

        logging.info('get rgb camera blueprint and set attribute')

        # Blueprintからカメラ情報を取得する
        camera_bp = self.world.get_blueprint_library().find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', str(width))
        camera_bp.set_attribute('image_size_y', str(height))
        camera_bp.set_attribute('fov', str(VIEW_FOV))
        return camera_bp

    def set_synchronous_mode(self, synchronous_mode):
        """
        Sets synchronous mode.
        """

        settings = self.world.get_settings()
        settings.synchronous_mode = synchronous_mode
        self.world.apply_settings(settings)

    def setup_car(self):
        """
        Spawns actor-vehicle to be controled.
        """
        logging.info('setup car info')

        car_bp = self.world.get_blueprint_library().filter('vehicle.*')[0]
        location = random.choice(self.world.get_map().get_spawn_points())
        self.car = self.world.spawn_actor(car_bp, location)

    def setup_camera(self, camera, width, height):
        """
        Spawns actor-camera to be used to render view.
        Sets calibration for client-side boxes rendering.
        """
        # カメラ取り付け位置調整
        #camera_transform = carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15))
        logging.info('setup camera1 (W,H)=({},{})'.format(width, height))
        camera_transform = carla.Transform(carla.Location(x=1.0, y=1, z=2.8), carla.Rotation(pitch=-15))
        self.camera = self.world.spawn_actor(self.camera_blueprint(width, height), camera_transform, attach_to=self.car)
        logging.info("test1")
        weak_self = weakref.ref(self)
        self.camera.listen(lambda image: weak_self().set_image(weak_self, image))
        
        logging.info('setup camera calibration1 start')

        calibration = np.identity(3)
        calibration[0, 2] = width / 2.0
        calibration[1, 2] = height / 2.0
        calibration[0, 0] = calibration[1, 1] = width / (2.0 * np.tan(VIEW_FOV * np.pi / 360.0))
        self.camera.calibration = calibration

        logging.info('setup camera calibration1 end')

    def setup_camera2(self, camera, width, height):
        """
        Spawns actor-camera to be used to render view.
        Sets calibration for client-side boxes rendering.
        """
        # カメラ取り付け位置調整
        #camera_transform = carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15))
        logging.info('setup camera2 (W,H)=({},{})'.format(width, height))
        camera_transform = carla.Transform(carla.Location(x=1.0, y=1.5, z=2.8), carla.Rotation(pitch=-15))
        self.camera2 = self.world.spawn_actor(self.camera_blueprint(width, height), camera_transform, attach_to=self.car)
        logging.info("test2")
        weak_self = weakref.ref(self)
        self.camera2.listen(lambda image: weak_self().set_image2(weak_self, image))
        
        logging.info('setup camera calibration2 start')

        calibration = np.identity(3)
        calibration[0, 2] = width / 2.0
        calibration[1, 2] = height / 2.0
        calibration[0, 0] = calibration[1, 1] = width / (2.0 * np.tan(VIEW_FOV * np.pi / 360.0))
        self.camera2.calibration = calibration

        logging.info('setup camera calibration2 end')

    def control(self, car):
        """
        Applies control to main car based on pygame pressed keys.
        Will return True If ESCAPE is hit, otherwise False to end main loop.
        """

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            return True

        control = car.get_control()
        control.throttle = 0
        if keys[K_w]:
            control.throttle = 1
            control.reverse = False
        elif keys[K_s]:
            control.throttle = 1
            control.reverse = True
        if keys[K_a]:
            control.steer = max(-1., min(control.steer - 0.05, 0))
        elif keys[K_d]:
            control.steer = min(1., max(control.steer + 0.05, 0))
        else:
            control.steer = 0
        control.hand_brake = keys[K_SPACE]

        car.apply_control(control)
        return False

    @staticmethod
    def set_image(weak_self, img):
        """
        Sets image coming from camera sensor.
        The self.capture flag is a mean of synchronization - once the flag is
        set, next coming image will be stored.
        """

        self = weak_self()
        if self.capture:
            self.image = img
            self.capture = False

    @staticmethod
    def set_image2(weak_self, img):
        """
        Sets image coming from camera sensor.
        The self.capture flag is a mean of synchronization - once the flag is
        set, next coming image will be stored.
        """

        self = weak_self()
        if self.capture2:
            self.image2 = img
            self.capture2 = False

    def render(self, display):
        """
        Transforms image from camera sensor and blits it to main pygame display.
        """

        if self.image is not None:
            array = np.frombuffer(self.image.raw_data, dtype=np.dtype("uint8"))
            array = np.reshape(array, (self.image.height, self.image.width, 4))
            array = array[:, :, :3]
            array = array[:, :, ::-1]
            surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
            display.blit(surface, (0, 0))

    def render2(self, display):
        """
        Transforms image from camera sensor and blits it to main pygame display.
        """

        if self.image2 is not None:
            array = np.frombuffer(self.image2.raw_data, dtype=np.dtype("uint8"))
            array = np.reshape(array, (self.image2.height, self.image2.width, 4))
            array = array[:, :, :3]
            array = array[:, :, ::-1]
            surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
            display.blit(surface, (self.image2.width, 0))

    def game_loop(self):
        """
        Main program loop.
        """

        try:
            # Pygameの初期化
            pygame.init()

            # クライアント部分の初期化
            self.client = carla.Client('127.0.0.1', 2000)
            # コネクト時間の設定
            self.client.set_timeout(2.0)
            # Worldの情報取得
            self.world = self.client.get_world()

            # 車の設定
            self.setup_car()
            # カメラの設定
            self.setup_camera(self.camera, VIEW_WIDTH, VIEW_HEIGHT)
            # カメラの設定
            self.setup_camera2(self.camera2, VIEW_WIDTH2, VIEW_HEIGHT2)

            self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
            #self.display2 = pygame.display.set_mode((VIEW_WIDTH2, VIEW_HEIGHT2), pygame.HWSURFACE | pygame.DOUBLEBUF)

            pygame_clock = pygame.time.Clock()

            self.set_synchronous_mode(True)
            vehicles = self.world.get_actors().filter('vehicle.*')

            logging.info("game loop start")
            # Game　Loop
            while True:
                self.world.tick()

                self.capture = True
                self.capture2 = True

                pygame_clock.tick_busy_loop(20)
                #logging.info("render start")

                self.render(self.display)

                #logging.info("bounding box start")

                bounding_boxes = ClientSideBoundingBoxes.get_bounding_boxes(vehicles, self.camera)

                #logging.info("bounding box draw")

                #ClientSideBoundingBoxes.draw_bounding_boxes(self.display, bounding_boxes)

                self.render2(self.display)

                bounding_boxes = ClientSideBoundingBoxes.get_bounding_boxes(vehicles, self.camera2)

                pygame.display.flip()

                pygame.event.pump()
                if self.control(self.car):
                    return

        finally:
            logging.warning('Pygame finally')

            self.set_synchronous_mode(False)
            self.camera.destroy()
            self.camera2.destroy()
            self.car.destroy()
            pygame.quit()


# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================


def main():
    """
    Initializes the client-side bounding box demo.
    """
    try:
        client = BasicSynchronousClient()
        client.game_loop()
    finally:
        logging.info('EXIT')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logging.warning('KeyboardInterrupt')
        pass



```