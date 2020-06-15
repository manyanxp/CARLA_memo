# CARLAのインストール他

# Reference

- [CARLA.org](https://carla.org/)
- [ROS Install](https://www.ros.org/install/)

# 1. CARLA
## 2. CARLAのインストール

#### a) deb CARLA インストール

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
#### b) パッケージインストール

[パッケージ](https://github.com/carla-simulator/carla/blob/master/Docs/download.md)

上記からダウンロードして、解凍すればOK。

Windowsの場合には、DirectXがインストールされていないと、CARLAのサーバーを立ち上げた際にDirectX Errorが発生する。Liunxの場合には、opengl指定が必要な場合があり。（要検証）

# 2. ROS

CARLAとROSを連携するために、まずはROSをインストールする。その後、CARLAとROSをブリッジさせるROSブリッジをインストールする。
先にROSが入っていない状態でROSブリッジをインストールしようとするとインストールできない可能性があるのて注意。

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
