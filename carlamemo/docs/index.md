# CARLAのインストール他

# Reference

- [CARLA.org](https://carla.org/)
- [ROS Install](https://www.ros.org/install/)

# 1. CARLA
## 1.1. CARLAのインストール

### a) deb CARLA インストール

システムにCARLA 0.9.9 repositoryを追加する。

```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 92635A407F7A020C
sudo add-apt-repository "deb [arch=amd64 trusted=yes] http://dist.carla.org/carla-0.9.9/ all main"
```

Install CARLA and check for the installation in the /opt/ folder.

```
sudo apt-get update
sudo apt-get install carla-simulator
cd /opt/carla-simulator
```
### b) パッケージインストール

[パッケージ](https://github.com/carla-simulator/carla/blob/master/Docs/download.md)

上記からダウンロードして、解凍すればOK。

Windowsの場合には、DirectXがインストールされていないと、CARLAのサーバーを立ち上げた際にDirectX Errorが発生する。Liunxの場合には、opengl指定が必要な場合があり。（要検証）

# 2. ROS

CARLAとROSを連携するために、まずはROSをインストールする。その後、CARLAとROSをブリッジさせるROSブリッジをインストールする。
先にROSが入っていない状態でROSブリッジをインストールしようとするとインストールできない可能性があるのて注意。

ref:[rosdep](http://wiki.ros.org/rosdep)

## 2.0. Pythonのバージョン

使用するROSがROS Kinetic/Melodicのとき、ROS MelodicはUbunutu 18.04、ROS KineticはUbunutu 16.04向けの
パッケージとなっている。

このとき、使用するROS MelodicかKineticを使用する場合には、Python2を使用する必要がある。
これは、ROS MelodicとKineticのrosdepがPython2(デフォルトでPython2向けの各種パッケージもインストールされる）向けで、Python3では動作しないようで、動作させるにはROSをNoeticにする必要があるが、ROS NetecはUbuntu20.04向けのようなので、使用するOS次第でROSが動作できな場合がある。



CARLA、ROSで動作させる必要があるのであれば、Python2 (Python 2.7 later)を使用することをおすすめします。

## 2.1. ROSのインストール

### 2.1.1. Configure your Ubuntu repositories

Ubuntuリポジトリを設定して、「制限付き」、「ユニバース」、「マルチバース」を許可する。この手順については、Ubuntuガイドを参照すること。

### 2.1.2. Setup your sources.list

packages.ros.orgからのソフトウェアを受け入れるようにコンピューターをセットアップする。

```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```

### 2.1.3. Set up your keys

```
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
```
### 2.1.4. インストール

1. まず、Debianパッケージインデックスが最新であることを確認する。

```
sudo apt update
```

2 .Desktop-Fullをインストールする。
　
```
sudo apt install ros-melodic-desktop
``` 

他にもパッケージが存在するが、必要なものがすべて入るので、一応、フルインストール版を選択する。
（ROSサイトもオススメしてる）

### 2.1.5. Environment setup

```
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
## 2.2. ROSブリッジのインストール

CARLAとROSで連携するための、ROSブリッジをインストールする。

ref:[ROS Bridge](https://github.com/carla-simulator/ros-bridge)

#### a) Using apt repository

aptレポジトリを追加する。

- Bridge for ROS Melodic.

```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 81061A1A042F527D &&
sudo add-apt-repository "deb [arch=amd64 trusted=yes] http://dist.carla.org/carla-ros-bridge-melodic/ bionic main"
```

今回は、Ubuntu 18.04向けのMelodicを使用する。
使用する場合は、ROSもMelodic向けを使用する。

ROSブリッジのインストール

```
sudo apt update &&
sudo apt install carla-ros-bridge-melodic
```

```
CUDA_VISIBLE_DEVICES=1 DISPLAY= ./CarlaUE4.sh -quality-level=Epic -opengl
```


## 未編集情報



## How to run an autoware

To run Autoware within CARLA please use the following execution order:

1. CARLA Server
2. Autoware (including carla-ros-bridge and additional nodes)

You need two terminals:

    #Terminal 1

    cd /opt/carla/bin
    ./CarlaUE4.sh

For details, please refer to the [CARLA documentation](https://carla.readthedocs.io/en/latest/).

    #Terminal 2

    export CARLA_MAPS_PATH=/opt/carla/HDMaps/

    source /opt/carla-ros-bridge/$ROS_DISTRO/setup.bash
    source ~/autoware.ai/install/setup.bash
    roslaunch carla_autoware_bridge carla_autoware_bridge_with_manual_control.launch




### NVIDIA Docker

- [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)
- [Autoware-AI Doccer](https://github.com/Autoware-AI/autoware.ai/wiki/Generic-x86-Docker)
- [Qiita Autoware 参考](https://qiita.com/misoragod/items/6d9ce990eb19c105dd96)

### issues
- [setting up with docker [still not working] #77](https://github.com/carla-simulator/carla-autoware/issues/77)
- [PythonAPI sensor actor cleanup "no stream available" #1821](https://github.com/carla-simulator/carla/issues/1821)

### How to bridge CARLA and Autoware

CARLAとAutowreの連携方法として、以下のドキュメントが公開されている。

[Autoware in Carla](https://github.com/carla-simulator/carla-autoware)

CARLAとAutowareを統合したものらしい。

現在は、[auteware.ai](https://github.com/Autoware-AI/autoware.ai)のリポジトリにシミュレーターのパッケージとして統合されているようで、[Autoware in Carla](https://github.com/carla-simulator/carla-autoware)は古い情報になる。

新しい情報を確認する場合には、[auteware.ai](https://github.com/Autoware-AI/autoware.ai)のリポジトリをクローンを行い以下の場所を確認。

```
 $ cd [install path]/autoware.ai/src/autoware/simulation
```

[2020/07/01]

[Could not install carla-hdmaps #2953](https://github.com/carla-simulator/carla/issues/2953)

autware.aiのsimulationディレクトリにあるREADME.mdの手順に従ってインストールすると、上記の問題が発生して、インストールが実行できない。


### Recommended skills you should have and recommend

- Docker
- Python
- C++
- Linux
- ROS

### 未整理

- [INTEGRATION OF AUTOWARE AND ROS](https://drive.google.com/file/d/1uO6nBaFirrllb08OeqGAMVLApQ6EbgAt/view)
- [carla-hdmaps](http://dist.carla.org/carla-hdmaps/pool/main/c/carla-hdmaps/)
- [Autoware-Manuals](https://github.com/CPFL/Autoware-Manuals)

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
