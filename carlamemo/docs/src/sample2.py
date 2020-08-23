from control.matlab import *
from matplotlib import pyplot as plt
import numpy as np

def main():
    print('PID制御器のパラメータ')
    # PID制御器のパラメータ
    Kp = 0.6  # 比例
    Ki = 0.03 # 積分
    Kd = 0.03 # 微分
    num = [Kd, Kp, Ki]
    den = [1, 0]
    K = tf(num, den)
    print("K = {}".format(K))
    print("")
    print("制御対象")
    # 制御対象
    Kt = 100      #定常ゲイン
    J = 0.01    #時定数
    C = 0.1     #むだ時間
    num = [Kt]  #分子の係数
    den = [J, C, 0] #分母の係数
    G = tf(num, den)
    print("")
    print("G = {}".format(G))

    time = 10 # (s)

    # フィードバックループ
    sys = feedback(K * G, 1)
    print("")
    print("sys {}".format(sys))

    t = np.linspace(0, time, 1000)
    print("")
    print("t {}".format(t))

    y, T = step(sys, t)

    # グラフ
    plt.plot(T, y)
    plt.grid()
    plt.axhline(Kt, color="b", linestyle="--")
    plt.xlim(0, time)
    plt.ylim(0, Kt+10)
    plt.xlabel("Time[sec.]")
    plt.ylabel("km/h")
    plt.show()

if __name__ == "__main__":
  main()
